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
from json2html import Json2Html
import logging
from vertexai.generative_models import FunctionDeclaration
from vertexai.preview.vision_models import ImageGenerationModel
from vertexai.preview import rag
import models.character
import models.game
import models.order
import models.product
import models.replay
import models.ticket
import models.user
from helpers.db_helper import getcursor, commit
from helpers.function_calling_helper import extract_text
import models

class User:
    def __init__(self, connection_pool, config_service, rag_model):
        self.connection_pool = connection_pool
        self.config_service = config_service
        self.rag_model = rag_model

    @staticmethod
    def get_function_declarations():
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

        request_refund = FunctionDeclaration(
            name="request_refund",
            description="Issue a refund for Cloud Gem or Cloud Gold",
            parameters={
                "type": "object",
                "properties": {
                    "game_title": {"type": "string", "description": "The name of the game to which the produced will be added"},
                    "product_title": {"type": "string", "description": "The name of the product to be purchased"},
                    "quantity": {"type": "string", "description": "Quantity of the purchased product"},
                },
                "required": [
                    "game_title",
                    "product_title",
                    "quantity",
                ]
            }
        )

        generate_profile_picture = FunctionDeclaration(
            name="generate_profile_picture",
            description="Create new profile picture or avatar with the description that user specifies.",
            parameters={
                "type": "object",
                "properties": {
                    "description": {"type": "string", "description": "Description of a profile picture"},
                },
                "required": [
                    "description",
                ]
            }
        )

        save_char_colors = FunctionDeclaration(
            name="save_char_colors",
            description="Save character's colors when user requests to update his character by name. Input are three colors in hex format",
            parameters={
                "type": "object",
                "properties": {
                    "char_name": {"type": "string", "description": "The name of the character user wants to change colors of"},
                    "c1": {"type": "string", "description": "Hex color 1"},
                    "c2": {"type": "string", "description": "Hex color 2"},
                    "c3": {"type": "string", "description": "Hex color 3"},
                    "c4": {"type": "string", "description": "Hex color 4"},
                },
                "required": [
                    "char_name",
                    "c1",
                    "c2",
                    "c3",
                    "c4",
                ]
            }
        )

        suggest_strategy = FunctionDeclaration(
            name="suggest_strategy",
            description="Make a suggestion in gameplay when user asks for tips or tricks or is looking for ways to improve",
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

        get_orders = FunctionDeclaration(
            name="get_orders",
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

        request_human_support = FunctionDeclaration(
            name="request_human_support",
            description="Ask for the support to be transferred to a human",
            parameters={
                "type": "object",
                "properties": {},            
            }
        )

        show_my_character = FunctionDeclaration(
            name="show_my_character",
            description="Show user's character on the screen.",
            parameters={
                "type": "object",
                "properties": {},            
            }
        )

        get_game_information = FunctionDeclaration(
            name="get_game_information",
            description="Use this function when asked about gameplay or game features of Cloud Royale or Droid shooter games.",
            parameters={
                "type": "object",
                "properties": {
                    "question_passthrough": {"type": "string", "description": "The whole user's prompt in the context of this message"}
                },
                "required": [
                    "question_passthrough",
                ]            
            }
        )

        return [
            generate_profile_picture,
            get_user_games,
            get_user_tickets,
            request_human_support,
            suggest_strategy,
            request_refund,
            get_orders,
            save_char_colors,
            show_my_character,
            get_game_information
        ]

    def get_game_information(self, user_id, question_passthrough):        
        response = self.rag_model.generate_content(question_passthrough)
        return extract_text(response)

    def suggest_strategy(self, user_id, game_title):
        try:
            with getcursor(self.connection_pool) as cur:
                cur.execute("SELECT * FROM available_games WHERE title ILIKE %s LIMIT 1", ["%" + str(game_title) + "%"])

            result = cur.fetchone()

            if result is None:
                return 'Product or game not found. Please try again.'

            game_object = models.game.Game.from_dict(result)

            cur.execute("SELECT * \
                FROM game_replays gr \
                JOIN users u ON gr.winner_id = u.user_id \
                WHERE gr.winner_id != %s AND gr.game_id = %s ORDER BY gr.winning_score DESC limit 1",
                    (user_id, game_object.game_id))

            result = cur.fetchone()

            if result is None:
                return 'Failed to find suitable winning replay. Please try again later.'
            
            user_object = models.user.User.from_dict(result)
            result['winner'] = user_object
            replay_object = models.replay.Replay.from_dict(result)

            message = f'Reply the user that you see they are having trouble getting a good score in {game_object.title}. \
                Tell the user to check the replay video with {replay_object.winning_score} points played on {replay_object.date}. \
                Add this raw HTML in the end: <br><br><iframe width="100%" height="320" src="{replay_object.replay_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>'
            
            return message
        
        except Exception as e:
            logging.error("%s, %s", traceback.format_exc(), e)
            return 'Reply that we failed to fetch an appliable game strategy.'

    def get_user_games(self, user_id):
        try:
            with getcursor(self.connection_pool) as cur:
                cur.execute("SELECT ag.game_id as game_id, ag.title as title , ag.description as description, purchase_date, ag.is_active as is_active \
                            FROM public.user_games AS ug LEFT JOIN available_games as ag ON ug.game_id = ag.game_id where ug.user_id = %s", 
                            [user_id])

                results = cur.fetchall()

            games = []
            for i in range(len(results)):
                games.append(models.game.Game.from_dict(results[i]))

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

            return html_table
        
        except Exception as e:
            logging.error("%s, %s", traceback.format_exc(), e)
            return 'Reply that we failed to fetch their games.'

    def get_user_tickets(self, user_id):
        try:
            with getcursor(self.connection_pool) as cur:
                cur.execute("SELECT ticket_id, user_id, ticket_type, message, created_at FROM user_tickets WHERE user_id = %s", [user_id])

            results = cur.fetchall()

            tickets = []
            for i in range(len(results)):
                tickets.append(models.ticket.Ticket.from_dict(results[i]))

            # Format the data for json2html
            formatted_data = [
                {
                    "Ticket Type": ticket.ticket_type,
                    "Message": ticket.message,
                    "Date": ticket.created_at
                }
                for ticket in tickets
            ]

            j2h = Json2Html()
            html_table = j2h.convert(json=formatted_data)

            html_table.__str__

            return html_table

        except Exception as e:
            logging.error("%s, %s", traceback.format_exc(), e)
            return 'Reply that we failed to fetch their tickets.'
        
    def get_orders(self, user_id, game_title):
        try:
            with getcursor(self.connection_pool) as cur:
                cur.execute("SELECT uo.*, ip.*, ag.* \
                    FROM user_orders uo \
                    JOIN ingame_products ip ON uo.product_id = ip.product_id \
                    JOIN available_games ag ON ip.game_id = ag.game_id \
                    WHERE uo.user_id = %s AND ag.title ILIKE %s;",
                        (user_id, "%" + str(game_title) + "%"))

            results = cur.fetchall()

            if len(results) == 0:
                return 'No orders were found for {game_title}.'

            orders = []
            for i in range(len(results)):
                product = models.product.Product.from_dict(results[i])
                game = models.game.Game.from_dict(results[i])
                results[i]['game'] = game
                results[i]['product'] = product
                orders.append(models.order.Order.from_dict(results[i]))

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

            return html_table
        except Exception as e:
            logging.error("%s, %s", traceback.format_exc(), e)
            return 'Reply that we failed to fetch their orders.'

    def request_refund(self, user_id, game_title, product_title, quantity): # not using date for now
        try:
            with getcursor(self.connection_pool) as cur:
                cur.execute("SELECT uo.*, ip.*, ag.* \
                    FROM user_orders uo \
                    JOIN ingame_products ip ON uo.product_id = ip.product_id \
                    JOIN available_games ag ON ip.game_id = ag.game_id \
                    WHERE uo.user_id = %s AND ag.title ILIKE %s AND ip.product_title ILIKE %s AND uo.quantity = %s LIMIT 1;",
                        (user_id, "%" + str(game_title) + "%", "%" + str(product_title) + "%", quantity))

            result = cur.fetchone()

            if result is None:
                return 'Failed to process their refund. Product or game not found. Ask them to try again.'

            product = models.product.Product.from_dict(result)
            game = models.game.Game.from_dict(result)

            message = f'Please issue a refund for {product.title}({product.product_id}) in {game.title}({game.game_id}). Requested quantity is {quantity}.'

            cur.execute(
                "INSERT INTO user_tickets (user_id, ticket_type, message, created_at) \
                    VALUES (%s, %s, %s, %s)",
                (user_id, 'billing', message, 'NOW()'),
            )

            commit(self.connection_pool)

            return 'Reply that we process refunds manually and that we have created a support ticket on their behalf.'
        except Exception as e:
            logging.error("%s, %s", traceback.format_exc(), e)
            return 'Reply saying that we failed to create a refund request support ticket. There was an internal error in our system. Ask them to try again.'

    def request_human_support(self, user_id):
        logging.info(f"Redirecting user {user_id}")
        return '<button onclick="window.location.href="\'https://www.google.com/\';">Contact Human Support</button>'

    def show_my_character(self, user_id):
        logging.info(f"Showing user's ({user_id}) Character")
        return 'Reply "There you go." and output this raw HTML: <script>$("#myCharacterWindow").show();</script>'

    def get_char_colors(self, user_id, char_name):
        try:
            with getcursor(self.connection_pool) as cur:
                cur.execute("SELECT * FROM character_personalization WHERE user_id = %s AND \
                             character_name ILIKE %s LIMIT 1", 
                             (user_id, "%" + str(char_name) + "%"))

            result = cur.fetchone()

            if result is None:
                return None

            character = models.character.Character.from_dict(result)

            return character.to_dict()
        
        except Exception as e:
            logging.error("%s, %s", traceback.format_exc(), e)
            return None

    def save_char_colors(self, user_id, char_name, c1, c2, c3, c4):

        try:
            with getcursor(self.connection_pool) as cur:
                cur.execute("UPDATE character_personalization SET c1 = %s, c2 = %s, c3 = %s, c4 = %s \
                            WHERE user_id = %s AND \
                             character_name ILIKE %s; COMMIT;", 
                             (c1, c2, c3, c4, user_id, "%" + str(char_name) + "%"))

            commit(self.connection_pool)

            return "Reply that their character colors have been saved."
        
        except Exception as e:
            logging.error("%s, %s", traceback.format_exc(), e)

            return 'Reply that we failed to update their character settings.'

    def generate_profile_picture(self, user_id, description):
        try:
            model = ImageGenerationModel.from_pretrained("imagen-3.0-fast-generate-001")

            images = model.generate_images(
                prompt=description + '. ' + self.config_service.get_property('chatbot', 'imagen_instructions'),
                # Optional parameters
                number_of_images=1,
                language="en",
                # You can't use a seed value and watermark at the same time.
                # add_watermark=False,
                # seed=100,
                aspect_ratio="1:1",
                safety_filter_level="block_some",
                person_generation="allow_adult",
            )

            output_file = "static/avatars/tmp-" + str(user_id) + "-" + str(random.randint(0, 10000)) + ".png"
            images[0].save(location=output_file, include_generation_parameters=False)        

            cdn_url = '/' + output_file
        except Exception as e:
            logging.error("%s, %s", traceback.format_exc(), e)
            return 'Reply that we failed to generate a new profile picture. Ask them to try again later'

        try:
            with getcursor(self.connection_pool) as cur:
                cur.execute(
                    "UPDATE users SET avatar = %s WHERE user_id = %s; COMMIT;",
                    (cdn_url, user_id),
                )

                commit(self.connection_pool)
                logging.info('Updated user profile picture to %s', cdn_url)
        except Exception as e:
            logging.error("%s, %s", traceback.format_exc(), e)
            return 'Reply that we failed to generate a new profile picture. Ask them to try again later'

        return 'Reply "There you go." and output this raw HTML: <br><img style="width: 50%; border-radius: 10px;" src="' + cdn_url + '"><br>'
        
