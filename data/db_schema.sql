CREATE TYPE TransactionType AS ENUM ('purchase', 'refund');
CREATE TYPE TicketType AS ENUM ('general', 'billing', 'account');

CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  email VARCHAR(255),
  password VARCHAR(64),
  is_active BOOLEAN DEFAULT FALSE,
  is_validated BOOLEAN DEFAULT FALSE
);

CREATE TABLE available_games (
  game_id SERIAL PRIMARY KEY,
  title VARCHAR(255),
  description TEXT,
  is_active BOOLEAN
);

CREATE TABLE ingame_products (
  product_id SERIAL PRIMARY KEY,
  game_id SERIAL REFERENCES available_games(game_id),
  title VARCHAR(255),
  description TEXT,
  price NUMERIC,
  is_active BOOLEAN
);

CREATE TABLE user_orders (
  user_id SERIAL REFERENCES users(user_id),
  game_id SERIAL REFERENCES available_games(game_id),
  product_id SERIAL,
  total_price NUMERIC,
  quantity INTEGER,
  transaction_type TransactionType,
  transaction_date DATE
);

CREATE TABLE user_games (
  user_id SERIAL REFERENCES users(user_id),
  game_id SERIAL REFERENCES available_games(game_id),
  purchase_date DATE,
  time_played INTEGER
);

CREATE TABLE user_tickets (
  user_id SERIAL REFERENCES users(user_id),
  ticket_type TicketType,
  message TEXT,
  created_at DATE
);
