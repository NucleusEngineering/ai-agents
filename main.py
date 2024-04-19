import vertexai
import requests, os

from vertexai.generative_models import (
    Content,
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    Part,
    Tool,
)
import psycopg2

from flask import Flask, request, jsonify, render_template

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
        description="Place an order of Gems, Coins or Gold for a games: Clash of Clans, Clash Royale, Boom Beach, Brawl Stars and Hay Day",
        parameters={
            "type": "object",
            "properties": {
                "product": {"type": "string", "description": "Product name"},
                "game": {"type": "string", "description": "Game name"},
            },
            "required": [
                "product",
                "game"
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

def place_order(user_id, product, game):
    try:
        # Write a function that inserts a new row into user_orders table in ai_agent postgresql database
        conn = psycopg2.connect(
            host="localhost",
            database="ai_agent",
            user="postgres",
            password="postgres",
        )

        # Create a cursor
        cur = conn.cursor()

        # Execute the query
        cur.execute(
            "INSERT INTO user_orders (user_id, product, game) VALUES (%s, %s, %s)",
            (user_id, product, game),
        )

        # Commit the transaction
        conn.commit()

        # Close the connection
        conn.close()

        return 1
    except Exception as e:
        print(e)
        return 0

def get_user_games(user_id):
    # Write a function that fetches all fields from user_games table in ai_agent postgresql database by user_id primary key
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host="localhost",
            database="ai_agent",
            user="postgres",
            password="postgres",
        )

        # Create a cursor
        cur = conn.cursor()

        # Execute the query
        cur.execute("SELECT ag.title, ag.description FROM public.user_games AS ug LEFT JOIN available_games as ag ON ug.game_id = ag.game_id where ug.user_id = %s", (user_id,))

        # Fetch the results
        results = cur.fetchall()

        # Close the connection
        conn.close()

        return results
    except Exception as e:
        print(e)
        return 0

def get_user_tickets(user_id):
    # Write a function that fetches all fields from user_tickets table in ai_agent postgresql database by user_id primary key
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host="localhost",
            database="ai_agent",
            user="postgres",
            password="postgres",
        )

        # Create a cursor
        cur = conn.cursor()

        # Execute the query
        cur.execute("SELECT * FROM user_tickets WHERE user_id = %s", (user_id,))

        # Fetch the results
        results = cur.fetchall()

        # Close the connection
        conn.close()

        return results
    except Exception as e:
        print(e)
        return 0

def request_human_support(user_id):
    # Swap gemini based chat to human based chat - redirect?
    return 0

def init_chat(model, user_id):
    chat_client = init()

    if user_id not in history_clients:
        history_clients[user_id] = []

    chat_client = model.start_chat(history=history_clients[user_id])
    return chat_client

def call_function(function_name, params):
    # TODO: hardcoded value for now
    params['user_id'] = 1

    try:
        return globals()[function_name](**params)
    except Exception as e:
        print(e)
        return 0

def extract_function(response):

    try:
        for part in response.candidates[0].content.parts: 
            if part.function_call.name:
                return part.function_call.name
    except Exception as e:
        print(e)

    return None

def extract_params(response):
    params = {}

    try:
        for part in response.candidates[0].content.parts: 
            for key, value in part.function_call.args.items():
                params[key[9:]] = value
    except Exception as e:
        print(e)
        params = {}

    return params

def extract_text(response):
    try:
        for part in response.candidates[0].content.parts: 
            if part.text:
                return part.text
    except Exception as e:
        return ""

# Initialize the model!!!!
model = init()

@app.route("/chat", methods=["POST"])
def chat():

    chat = init_chat(model, user_id)
    prompt = request.form.get("prompt") + PROMPT_SUFFIX

    response = chat.send_message([COC_FAQ, prompt])
    history_clients[user_id] = chat.history

    function_params = extract_params(response)
    function_name = extract_function(response)
    response_text = extract_text(response)

    if function_name:
        print("Calling  " + function_name)
        func_response = call_function(function_name, function_params)
        response = chat.send_message(
                Part.from_function_response(
                name=function_name,
                response={
                    "content": func_response,
                },
            ),
        )

        response_text += '. ' + extract_text(response)
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
