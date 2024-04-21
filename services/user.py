import psycopg2
from psycopg2.extras import RealDictCursor
from models import ticket, game

class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def get_user_games(user_id):
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="ai_agent",
                user="postgres",
                password="postgres",
            )

            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT ag.game_id as game_id, ag.title as title , ag.description as description, ag.is_active as is_active \
                        FROM public.user_games AS ug LEFT JOIN available_games as ag ON ug.game_id = ag.game_id where ug.user_id = %s", 
                        (user_id,))

            results = cur.fetchall()
            games = ''

            if len(results) > 0:
                for result in results:
                    games +=  game.Game.from_dict(result) + '\n'

            conn.close()

            return games
        except Exception as e:
            print(e)
            return 0

    def get_user_tickets(user_id):
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="ai_agent",
                user="postgres",
                password="postgres",
            )

            cur = conn.cursor(cursor_factory=RealDictCursor)

            cur.execute("SELECT user_id, ticket_type, message, created_at FROM user_tickets WHERE user_id = %s", (user_id,))

            results = cur.fetchall()

            conn.close()

            tickets = ''

            if len(results) > 0:
                for result in results:
                    tickets +=  ticket.Ticket.from_dict(result) + '\n'

            return tickets

        except Exception as e:
            print(e)
            return 0


    def place_order(user_id, game, product, quantity):
        if quantity is None:
            quantity = 1

        product_id = 1
        total_price = 10

        try:
            conn = psycopg2.connect(
                host="localhost",
                database="ai_agent",
                user="postgres",
                password="postgres",
            )

            cur = conn.cursor(cursor_factory=RealDictCursor)

            cur.execute("SELECT ag.game_id, ip.price, ip.title, ip.price, ip.product_id FROM available_games AS ag \
                        LEFT JOIN ingame_products AS ip ON ag.game_id = ip.game_id WHERE \
                        ag.title LIKE %s AND ip.title LIKE %s LIMIT 1",
                        ('%'+game+'%', '%'+product+'%'))

            result = cur.fetchone()

            if result is None:
                return 'Failed to place your order. Product or game not found. Please try again.'

            game_id = result['game_id']
            product_id = result['product_id']
            total_price = float(result['price']) * float(quantity)

            cur.execute(
                "INSERT INTO user_orders (game_id, user_id, product_id, total_price, quantity, transaction_type, transaction_date) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (game_id, user_id, product_id, total_price, quantity, 'purchase', 'NOW()'),
            )

            conn.commit()

            conn.close()

            return f'Order placed successfully for {product} in {game} for a total price of {total_price}. You will receive a confirmation email shortly'
        except Exception as e:
            print(e)
            return 'Failed to place your order. There was an internal error in our system. Please try again.'

    def request_human_support(user_id):    
        return 'You will be redirected to a human support agent shortly. Please wait.'

