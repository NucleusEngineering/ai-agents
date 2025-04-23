-- Copyright 2024 Google LLC
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--      https://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.

CREATE TYPE TransactionType AS ENUM ('purchase', 'refund');
CREATE TYPE TicketType AS ENUM ('general', 'billing', 'account');

CREATE TABLE users (
  user_id uuid PRIMARY KEY,
  name VARCHAR(255),
  email VARCHAR(255),
  password VARCHAR(64),
  avatar TEXT,
  is_active BOOLEAN DEFAULT FALSE,
  is_validated BOOLEAN DEFAULT FALSE
);

INSERT INTO users (user_id, name, email, password, is_active, is_validated) VALUES
('7608dc3f-d239-405c-a097-b152ab38a354',	'Test User 1',	'test-user-1@domain.tld',	encode(sha256('password'), 'hex'),	't',	't');

CREATE TABLE available_games (
  game_id SERIAL PRIMARY KEY,
  title VARCHAR(255),
  description TEXT,
  is_active BOOLEAN
);

INSERT INTO available_games (game_id, title, description, is_active) VALUES
(1,	'Cloud Meow',	'Cloud Meow is a game about solving puzzles with help of google cloud.',	't');


CREATE TABLE ingame_products (
  product_id SERIAL PRIMARY KEY,
  game_id SERIAL REFERENCES available_games(game_id),
  product_title VARCHAR(255),
  product_description TEXT,
  product_price NUMERIC,
  is_product_active BOOLEAN
);

INSERT INTO ingame_products (product_id, game_id, product_title, product_description, product_price, is_product_active) VALUES
(1,	1,	'Paw Token', 'Token to help you unlock a hint', 1.49, 't'),
(2,	1,	'Poop token', 'Special token that allows yu to undo whenever you do a mistake',	1.99, 't');


CREATE TABLE game_replays (
  replay_id SERIAL PRIMARY KEY,
  game_id SERIAL REFERENCES available_games(game_id),
  winning_score NUMERIC,
  replay_url VARCHAR(2048),
  winner_id uuid REFERENCES users(user_id),
  game_date DATE
);

INSERT INTO game_replays (replay_id, game_id, winning_score, replay_url, winner_id, game_date) VALUES
(1,	1,	123, 'https://www.youtube.com/embed/4D3X6Xl5c_Y', '7608dc3f-d239-405c-a097-b152ab38a354', CURRENT_DATE);

CREATE TABLE user_orders (
  order_id SERIAL PRIMARY KEY,
  user_id uuid REFERENCES users(user_id),
  game_id SERIAL REFERENCES available_games(game_id),
  product_id SERIAL,
  total_price NUMERIC,
  quantity INTEGER,
  transaction_type TransactionType,
  transaction_date DATE
);

INSERT INTO public.user_orders(order_id, user_id, game_id, product_id, total_price, quantity, transaction_type, transaction_date) VALUES 
(1, '7608dc3f-d239-405c-a097-b152ab38a354', 1, 1, 12.3, 10, 'purchase', CURRENT_DATE),
(2, '7608dc3f-d239-405c-a097-b152ab38a354', 1, 2, 23.8, 20, 'purchase', CURRENT_DATE);

CREATE TABLE user_games (
  user_id uuid REFERENCES users(user_id),
  game_id SERIAL REFERENCES available_games(game_id),
  purchase_date DATE,
  time_played NUMERIC
);

INSERT INTO user_games (user_id, game_id, purchase_date, time_played) VALUES
('7608dc3f-d239-405c-a097-b152ab38a354',	1,	CURRENT_DATE, 100);

CREATE TABLE user_tickets (
  ticket_id SERIAL PRIMARY KEY,
  user_id uuid REFERENCES users(user_id),
  ticket_type TicketType,
  message TEXT,
  created_at DATE
);

INSERT INTO user_tickets (user_id, ticket_type, message, created_at) VALUES
('7608dc3f-d239-405c-a097-b152ab38a354',	'general', 'Just wanted to ask you about any other upcoming games. Thank you!',	CURRENT_DATE);
