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
import random
import logging
import requests, json
import time
import threading
import base64

from json2html import Json2Html

from common.function_calling import extract_text
from common.rag import RAG
from common.db_helper import getcursor, commit
from models import model, user, game, replay, order, product

from google.cloud.firestore_v1.base_query import FieldFilter
from google.cloud.firestore_v1.client import Client

from google import genai
from google.genai import types
from vertexai.preview.vision_models import ImageGenerationModel

from flask_socketio import SocketIO
from psycopg2.pool import SimpleConnectionPool

class User:
    def __init__(self, db: Client, alloydb: SimpleConnectionPool, config_service, gemini_client: genai.Client, socketio: SocketIO):
        """
        Initializes the User service.

        Args:
            db: Firestore client instance.
            config_service: Service to get configuration values.
            rag_config: The RAG model instance.
        """
        self.db = db
        self.alloydb = alloydb
        self.config_service = config_service
        self.gemini_client = gemini_client
        self.socketio = socketio


    @staticmethod
    def get_function_declarations():

        fc_generate_avatar = types.FunctionDeclaration(
            name='fc_generate_avatar',
            description='Create new avatar or avatar. Inject the description into the function that is being called.',
            parameters=types.Schema(
                type='OBJECT',
                properties={
                    'description': types.Schema(
                        type='string', 
                        description='Description of the picture or avatar',
                    ),
                },
                required=[
                    'description',
                ]
            ),
        )

        fc_rag_retrieval = types.FunctionDeclaration(
            name='fc_rag_retrieval',
            description='Function to be invoked when the prompt is about a super secret game called Cloud Meow.',
            parameters=types.Schema(
                type='OBJECT',
                properties={
                    'question_passthrough': types.Schema(
                        type='string', 
                        description='The whole user\'s prompt in the context of this message'
                    )
                },
                required=[
                    'question_passthrough',
                ]            
            )
        )

        fc_save_model_color = types.FunctionDeclaration(
            name='fc_save_model_color',
            description='Save new color when user requests to update his game model. Input is a color in hex format',
            parameters=types.Schema(
                type='OBJECT',
                properties={
                    'color': types.Schema(
                        type='string', 
                        description='Hex color'
                    )
                },
                required=[
                    'color',
                ]
            )
        )        

        fc_revert_model_color = types.FunctionDeclaration(
            name='fc_revert_model_color',
            description='Revert the color/material of user\'s model on their request.',
            parameters=types.Schema(
                type='OBJECT',
                properties={}
            )
        )        

        fc_show_my_model = types.FunctionDeclaration(
            name='fc_show_my_model',
            description='Show user\'s model / character on the screen.',
            parameters=types.Schema(
                type='OBJECT',
                properties={},            
            )
        )
        
        fc_show_my_avatar = types.FunctionDeclaration(
            name='fc_show_my_avatar',
            description='Show user\'s current avatar.',
            parameters=types.Schema(
                type='OBJECT',
                properties={}
            )
        )

        fc_get_user_games = types.FunctionDeclaration(
            name="fc_get_user_games",
            description="Get the games that the user has purchased",
            parameters={
                "type": "object",
                "properties": {},            
            }
        )

        fc_suggest_strategy = types.FunctionDeclaration(
            name="fc_suggest_strategy",
            description="Make a suggestion in gameplay when user asks for a strategy to win.",
            parameters={
                "type": "object",
                "properties": {
                    "game_title": {"type": "string", "description": "The name of the game which user needs help with"},
                },
                "required": [
                    "game_title",
                ]
            },
        )

        fc_get_orders = types.FunctionDeclaration(
            name="fc_get_orders",
            description="Get a list of orders based on the name of the game provided by the user.",
            parameters={
                "type": "object",
                "properties": {
                    "game_title": {"type": "string", "description": "The name of the game of which the orders should be fetched"}
                },
                "required": [
                    "game_title",
                ]
            },
        )        


        return types.Tool(function_declarations=[
            fc_get_orders,
            fc_suggest_strategy,
            fc_get_user_games,
            fc_generate_avatar,
            fc_rag_retrieval,
            fc_save_model_color,
            fc_revert_model_color,
            fc_show_my_model,
            fc_show_my_avatar
        ])
    
    def fc_save_model_color(self, color, user_id):
        """
        Saves the model's color to Firestore.

        Args:
            user_id: The ID of the user.
            color: The hex color to save.

        Returns:
            A string response for the user.
        """
        try:
            # Get the models collection reference
            models_ref = self.db.collection("models")

            # Query for the model with the given user_id
            query = models_ref.where(filter=FieldFilter("user_id", "==", user_id))
            results = query.get()

            if not results:
                return f"Reply that no character for user '{user_id}' was found."

            # Update the color of the first matching document
            for doc in results:
                doc.reference.update({"color": color, "original_material": False})
                logging.info(f"Updated color to '{color}' for '{user_id}'\'s model.")
                break

            return '''Reply that their character color has been updated''', '''<script>window.reloadCurrentModel();</script>'''
        
        except Exception as e:
            logging.error("%s, %s", traceback.format_exc(), e)
            return 'Reply that we failed to update their character settings.'

    
    def fc_revert_model_color(self, user_id):
        """
        Revert's the model's color.

        Args:
            user_id: The ID of the user.

        Returns:
            A string response for the user.
        """
        try:
            # Get the models collection reference
            models_ref = self.db.collection("models")

            # Query for the model with the given user_id
            query = models_ref.where(filter=FieldFilter("user_id", "==", user_id))
            results = query.get()

            if not results:
                return f"Reply that no character for user '{user_id}' was found."

            # Update the color of the first matching document
            for doc in results:
                doc.reference.update({"original_material": True})
                logging.info(f"Reverted to original materials for '{user_id}'\'s model.")
                break

            return '''Reply that their character colors have been reverted''', '''<script>window.reloadCurrentModel();</script>'''
        
        except Exception as e:
            logging.error("%s, %s", traceback.format_exc(), e)
            return 'Reply that we failed to update their character settings.'

    def fc_generate_avatar(self, description, user_id):
        """Returns the new avatar for the user.

        Args:
        description: The description of the avatar to be generated
        """
        try:
            model = ImageGenerationModel.from_pretrained(self.config_service.get_property("general", "imagen_version"))

            instruction = self.config_service.get_property("chatbot", "diffusion_generation_instruction")

            images = model.generate_images(
                prompt=instruction % description,
                number_of_images=4,
                language="en",
                seed=100,
                add_watermark=False,
                aspect_ratio="1:1",
                safety_filter_level="block_some",
                person_generation="allow_adult",
            )

            output_file = "static/avatars/" + str(user_id) + ".png"
            images[0].save(location=output_file, include_generation_parameters=False)        

            cdn_url = '/' + output_file
        except Exception as e:
            logging.info("%s, %s", traceback.format_exc(), e)
            return 'Reply that we failed to generate a new avatar. Ask them to try again later'


        try:
            # Update Firestore "users" collection
            user_ref = self.db.collection("users").where(filter=FieldFilter("user_id", "==", user_id))
            user_ref.get()[0].reference.update({"avatar": cdn_url})
            logging.info('Updated user avatar to %s', cdn_url)
        except Exception as e:
            logging.info("%s, %s", traceback.format_exc(), e)
            return 'Reply that we failed to generate a new avatar. Ask them to try again later'

        return '''Reply something like "There you go."''', '''
            <div>
                <br>
                <img class="avatar" src="%s?rand=%s">
            </div>''' % (cdn_url, str(random.randint(0, 1000000)))

    def fc_rag_retrieval(self, question_passthrough, user_id):
        """
        Retrieves information using RAG model.

        Args:
            user_id: The ID of the user.
            question_passthrough: The user's prompt.

        Returns:
            The RAG model's response as a string.
        """

        # Additional rag config

        response = self.gemini_client.models.generate_content(
            model=self.config_service.get_property('general', 'rag_gemini_version'),
            contents=question_passthrough,
            config=types.GenerateContentConfig(
                system_instruction=self.config_service.get_property('chatbot', 'llm_system_instruction') + self.config_service.get_property('chatbot', 'llm_response_type'),
                tools=[RAG(self.config_service).get_rag_retrieval()]    
            )
        )

        print(response)

        return response.text, ''

    def fc_show_my_model(self, user_id):
        logging.info(f"Showing user's ({user_id}) character")
        return '''Reply something like "there you go"''', '''<script>window.reloadCurrentModel(); $("#modelWindow").show();</script>'''

    def fc_show_my_avatar(self, user_id):
        logging.info(f"Showing user's ({user_id}) avatar")
        return '''Reply something like "There you go."''', '''
            <div>
                <br>
                <img class="avatar" src="/static/avatars/%s.png?rand=%s">
            </div>''' % (user_id, str(random.randint(0, 1000000)))


    def fc_get_orders(self, user_id, game_title):
        try:
            with getcursor(self.alloydb) as cur:
                cur.execute("SELECT uo.*, ip.*, ag.* \
                    FROM user_orders uo \
                    JOIN ingame_products ip ON uo.product_id = ip.product_id \
                    JOIN available_games ag ON ip.game_id = ag.game_id \
                    WHERE uo.user_id = %s AND ag.title ILIKE %s;",
                        (user_id, "%" + str(game_title) + "%"))

            results = cur.fetchall()

            if len(results) == 0:
                return 'No orders were found for {game_title}.', ""

            orders = []
            for i in range(len(results)):
                _product = product.Product.from_dict(results[i])
                _game = game.Game.from_dict(results[i])
                results[i]['game'] = _game
                results[i]['product'] = _product
                orders.append(order.Order.from_dict(results[i]))

            # Format the data for json2html
            formatted_data = [
                {
                    "Game Title": order.game.title,
                    "Product Title": order.product.title,
                    "Total Price": order.total_price,
                    "Quantity": order.quantity,
                    "Transaction Date": order.transaction_date,
                }
                for order in orders
            ]

            j2h = Json2Html()
            html_table = j2h.convert(json=formatted_data)

            html_table.__str__

            return "Reply something like 'Here are you orders:'", html_table
        except Exception as e:
            logging.error("%s, %s", traceback.format_exc(), e)
            return 'Reply that we failed to fetch their orders.', ""

    def fc_get_user_games(self, user_id):
        try:
            with getcursor(self.alloydb) as cur:
                cur.execute("SELECT ag.game_id as game_id, ag.title as title , ag.description as description, purchase_date, ag.is_active as is_active \
                            FROM public.user_games AS ug LEFT JOIN available_games as ag ON ug.game_id = ag.game_id where ug.user_id = %s", 
                            [user_id])

                results = cur.fetchall()

            games = []
            for i in range(len(results)):
                games.append(game.Game.from_dict(results[i]))

            # Format the data for json2html
            formatted_data = [
                {
                    "Title": game.title,
                    "Description": game.description
                }
                for game in games
            ]

            j2h = Json2Html()
            html_table = j2h.convert(json=formatted_data)
            html_table.__str__

            return 'Reply something like "Here are you games:"', html_table

        
        except Exception as e:
            logging.error("%s, %s", traceback.format_exc(), e)
            return 'Reply that we failed to fetch their games.', ""

    def fc_suggest_strategy(self, user_id, game_title):
        try:
            with getcursor(self.alloydb) as cur:
                cur.execute("SELECT * FROM available_games WHERE title ILIKE %s LIMIT 1", ["%" + str(game_title) + "%"])

            result = cur.fetchone()

            if result is None:
                return 'Product or game not found. Please try again.', ""

            game_object = game.Game.from_dict(result)

            cur.execute("SELECT * \
                FROM game_replays as gr \
                WHERE gr.game_id = %s ORDER BY gr.winning_score DESC limit 1",
                    [game_object.game_id])
            
            result = cur.fetchone()

            if result is None:
                return 'Failed to find suitable winning replay. Please try again later.', ""
            
            result['winner'] = "Anonymous"
            replay_object = replay.Replay.from_dict(result)

            message = f'Reply the user that you see they are having trouble getting a good score in {game_object.title}. \
                Tell the user to check the replay video with {replay_object.winning_score} points played on {replay_object.date}.'
            
            html_out = f'''<br>
            <br>
            <iframe 
                width="100%" height="320" 
                src="{replay_object.replay_url}" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                referrerpolicy="strict-origin-when-cross-origin" 
                allowfullscreen>
            </iframe>'''

            return message, html_out
        
        except Exception as e:
            logging.error("%s, %s", traceback.format_exc(), e)
            return 'Reply that we failed to fetch an appliable game strategy.', ""


    def get_model(self, user_id):
        """
        Retrieves the color of a character from Firestore.

        Args:
            user_id: The ID of the user.

        Returns:
            A dictionary containing the character's color information, or None if not found.
        """
        try:
            # Get the models collection reference
            models_ref = self.db.collection("models")

            # Query for the model with the given user_id
            query = models_ref.where("user_id", "==", user_id)
            results = query.get()

            if not results:
                logging.warning(f"No character found for '{user_id}'.")
                return None

            return model.Model.from_dict(results[0].to_dict())

        except Exception as e:
            logging.error("%s, %s", traceback.format_exc(), e)
            return None
        

