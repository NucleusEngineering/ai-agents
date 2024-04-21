import vertexai
import os

from vertexai.generative_models import (
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    Part,
    Tool,
)
from flask import Flask, request, jsonify, render_template
from utils import function_calling_tools

# Environment variables

PROJECT_ID = "dn-demos"
LOCATION = "us-central1"  # @param {type:"string"}
SYSTEM_TEXT = """You are an AI assistant called SuperAgent. 
    Only answer when you know. 
    You can also call functions that were supplied to you.     
    You only know about Clash of Clans and other games that you get from function calling. 
    You rely on the ClashOfClansFAQ.pdf document provided to you to answer questions about Clash of Clans.
    """  # @param {type:"string"}

COC_FAQ = Part.from_uri(
    mime_type="application/pdf",
    uri="gs://ai-agent-data-bucket/ClashOfClansFAQ.pdf")

PROMPT_SUFFIX = "\n Please format the message as a support agent would."

## Flask app

app = Flask(
    __name__,
    instance_relative_config=True,
    template_folder="templates",
)

history_clients = {}
user_id = 1 # Hardcoded user_id for testing

vertexai.init(project=PROJECT_ID, location=LOCATION)

def init():
    get_user_games = FunctionDeclaration(
        name="get_user_games",
        description="Get the games that the user has purchased",
        parameters={
            "type": "object",
            "properties": {},            
        }
    )

    get_user_tickets = FunctionDeclaration(
        name="get_user_tickets",
        description="Get the tickets that the user has opened with support",
        parameters={
            "type": "object",
            "properties": {},            
        }
    )

    request_human_support = FunctionDeclaration(
        name="request_human_support",
        description="Ask for the support to be transferred to a human",
        parameters={
            "type": "object",
            "properties": {},            
        }
    )

    place_order = FunctionDeclaration(
        name="place_order",
        description="Place an order for products like Cloud Gem or Cloud Gold for games such as Droid Shooter or Cloud Royale games. Product names shoud be sigular and not plural.",
        parameters={
            "type": "object",
            "properties": {
                "game": {"type": "string", "description": "The name of the game to which the produced will be added"},
                "product": {"type": "string", "description": "The name of the product to be purchased"},
                "quantity": {"type": "integer", "description": "Quantity of the purchased product"},
            },
            "required": [
                "game",
                "product",
                "quantity",
            ]
        },
    )

    retail_tool = Tool(
        function_declarations=[
            get_user_games,
            get_user_tickets,
            request_human_support,
            place_order
        ],        
    )

    model = GenerativeModel(
        "gemini-1.5-pro-preview-0409",
        generation_config=GenerationConfig(temperature=0),
        tools=[retail_tool],
        system_instruction=[SYSTEM_TEXT]
    )

    return model

def init_chat(model, user_id):
    chat_client = init()

    if user_id not in history_clients:
        history_clients[user_id] = []

    chat_client = model.start_chat(history=history_clients[user_id])
    return chat_client

model = init()

@app.route("/chat", methods=["POST"])
def chat():

    chat = init_chat(model, user_id)
    prompt = request.form.get("prompt") + PROMPT_SUFFIX

    response = chat.send_message([COC_FAQ, prompt])
    history_clients[user_id] = chat.history

    print(response)

    function_params = function_calling_tools.extract_params(response)
    function_name = function_calling_tools.extract_function(response)
    response_text = function_calling_tools.extract_text(response)

    if function_name:
        print("Calling  " + function_name)
        func_response = function_calling_tools.call_function(function_name, function_params)
        response = chat.send_message(
                Part.from_function_response(
                name=function_name,
                response={
                    "content": func_response,
                },
            ),
        )

        response_text += '. ' + function_calling_tools.extract_text(response)
    else:
        print('No function to be called...')

    return jsonify({"response": response_text})

@app.route("/version", methods=["GET"])
def version():
    return "v0.1"

@app.route("/", methods=["GET"])
def home():
    # return contents of index.html in the same folder
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8888)))
