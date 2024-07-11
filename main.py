# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import traceback
import vertexai
import os
import logging
import subprocess

import vertexai.preview.generative_models as generative_models

from vertexai.preview.generative_models import (
    GenerationConfig,
    GenerativeModel,
    Part,
    Tool,
)

from flask import Flask, request, jsonify
from helpers import db_helper, function_calling_helper, generic_helper, rag_helper

from services.user import User as UserService
from models.user import User as UserModel

# Environment variables

PROJECT_ID = os.environ.get("PROJECT_ID", "<GCP_PROJECT_ID>")
REGION = os.environ.get("REGION", "<GCP_REGION>")

SAFETY_SETTINGS = {
    generative_models.HarmCategory.HARM_CATEGORY_UNSPECIFIED: generative_models.HarmBlockThreshold.BLOCK_NONE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_NONE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_NONE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_NONE,
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_NONE,
}

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

vertexai.init(project=PROJECT_ID, location=REGION)

config = generic_helper.Config.get_instance()
rag = rag_helper.RAG(config)

def init_model():
    retail_tool = Tool(
        function_declarations=UserService.get_function_declarations(),        
    )

    model = GenerativeModel(
        config.get_property('general', 'gemini_version'),
        tools=[retail_tool],
        generation_config=GenerationConfig(temperature=1),
        system_instruction=[config.get_property('chatbot', 'llm_system_instruction')]
    )

    return model

def init_flash_model():
    model = GenerativeModel(
        config.get_property('general', 'gemini_flash_version'),
        generation_config=GenerationConfig(temperature=1)
    )

    return model

def init_rag_model(): 
    rag_retrieval_tool = Tool.from_retrieval(
        rag.get_rag_retrieval()
    )
    # Create a gemini-pro model instance
    model = GenerativeModel(
        model_name=config.get_property('general', 'gemini_flash_version'), 
        tools=[rag_retrieval_tool]
    )

    return model


# Chat initialization per tenant (cleanup needed after timeout/logout)
def init_chat(model, user_id):
    if user_id in client_sessions:
        logging.debug("Re-using existing session")
        return client_sessions[user_id]

    logging.debug("Creating new chat session for user %s", user_id)

    if user_id not in history_clients:
        history_clients[user_id] = []

    chat_client = model.start_chat(history=history_clients[user_id])

    client_sessions[user_id] = chat_client
    return client_sessions[user_id]

# Init models 
chat_model = init_model()
audio_model = init_flash_model()
rag_model = init_rag_model()

# Init services
db = db_helper.init_db()
user_service = UserService(db, generic_helper.Config.get_instance(), rag_model)

# Init our session handling variables
client_sessions = {}
history_clients = {}

# Hardcoded user for testing. Proper authentication is needed.
user = UserModel.from_dict({
        "user_id": 1,
        "email": "test-user-1@domain.tld",
        "name": "Test User 1",
        "avatar": "",
        "is_active": "true",
        "is_validated": "true",
})

app = Flask(
    __name__,
    instance_relative_config=True,
#    template_folder="templates",
)

# Our main chat handler
@app.route("/chat", methods=["POST"])
def chat():
    chat = init_chat(chat_model, user.user_id)
    audio = generic_helper.get_audio_stream(request)

    # If we got audio stream input, let's convert it first to text via gemini flash
    if audio != None: 
        audio_prompt = Part.from_data(audio, 'audio/mpeg')
        transcribed_audio_response = audio_model.generate_content(
            [config.get_property('chatbot', 'audio_transcription_instruction'), audio_prompt]
        )
        
        transcribed_audio = function_calling_helper.extract_text(transcribed_audio_response)
        logging.debug(f"Transcribed audio: %s", transcribed_audio)
        
        # Now that we have the audio in text for, so we can send it further to our pipeline
        response = chat.send_message(
            transcribed_audio,
            safety_settings=SAFETY_SETTINGS,
        )

    else:
        prompt = Part.from_text(request.form.get("prompt"))
        response = chat.send_message(
            prompt,
            safety_settings=SAFETY_SETTINGS,
        )

    history_clients[user.user_id] = chat.history

    function_params = function_calling_helper.extract_params(response)
    function_name = function_calling_helper.extract_function(response)
    text_response = function_calling_helper.extract_text(response)

    if function_name:
        try:
            logging.info("Calling  " + function_name)
            
            # Injection of user_id (this should be done dynamically when proper auth is implemented)
            function_params['user_id'] = user.user_id
            function_response = function_calling_helper.call_function(user_service, function_name, function_params)

            response = chat.send_message(
                    Part.from_function_response(
                    name=function_name,
                    response={
                        "content": function_response,
                    },
                ),
                safety_settings=SAFETY_SETTINGS     
            )

            text_response = function_calling_helper.extract_text(response)

        except Exception as e:
            logging.error("%s, %s", traceback.format_exc(), e)
            text_response = 'Sorry, I couldn\'t process your query. Please try again later.'

    if len(text_response) == 0:
        text_response = 'Sorry, I couldn\'t process your query. Please try again later.'
        
    return generic_helper.gemini_response_to_template_html(text_response)

# Get character color
@app.route("/get_color/<char_name>", methods=["GET"])
def get_color(char_name):
    colors = user_service.get_char_colors(user.user_id, char_name)

    if(colors) :
        response = jsonify(colors)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
    return 'Character was not found. Double-check the name and try again.', 404

@app.route("/", methods=["GET"])
def home():
    with open("templates/index.html", mode='r') as file: #
        data = file.read()

    return data
    # return render_template("index.html")

@app.route("/model", methods=["GET"])
def model():
    with open("templates/model.html", mode='r') as file:
        data = file.read()

    return data
    # return render_template("model.html")

@app.route("/version", methods=["GET"])
def version():
    return jsonify({
        "version": config.get_property('general', 'version')
        })

if __name__ == "__main__":
    os.makedirs('uploads', exist_ok=True)
    rc = subprocess.call("create-schema.sh")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8888)))
