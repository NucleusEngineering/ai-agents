--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2 (Debian 16.2-1.pgdg110+2)
-- Dumped by pg_dump version 16.2 (Debian 16.2-1.pgdg110+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: tickettype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.tickettype AS ENUM (
    'general',
    'billing',
    'account'
);


ALTER TYPE public.tickettype OWNER TO postgres;

--
-- Name: transactiontype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.transactiontype AS ENUM (
    'purchase',
    'refund'
);


ALTER TYPE public.transactiontype OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: available_games; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.available_games (
    game_id integer NOT NULL,
    title character varying(255),
    description text,
    is_active boolean
);


ALTER TABLE public.available_games OWNER TO postgres;

--
-- Name: available_games_game_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.available_games_game_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.available_games_game_id_seq OWNER TO postgres;

--
-- Name: available_games_game_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.available_games_game_id_seq OWNED BY public.available_games.game_id;


--
-- Name: ingame_products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ingame_products (
    product_id integer NOT NULL,
    game_id integer NOT NULL,
    title character varying(255),
    description text,
    price numeric,
    is_active boolean
);


ALTER TABLE public.ingame_products OWNER TO postgres;

--
-- Name: ingame_products_game_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ingame_products_game_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ingame_products_game_id_seq OWNER TO postgres;

--
-- Name: ingame_products_game_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ingame_products_game_id_seq OWNED BY public.ingame_products.game_id;


--
-- Name: ingame_products_product_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ingame_products_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ingame_products_product_id_seq OWNER TO postgres;

--
-- Name: ingame_products_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ingame_products_product_id_seq OWNED BY public.ingame_products.product_id;


--
-- Name: user_games; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_games (
    user_id integer NOT NULL,
    game_id integer NOT NULL,
    purchase_date date,
    time_played integer
);


ALTER TABLE public.user_games OWNER TO postgres;

--
-- Name: user_games_game_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_games_game_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_games_game_id_seq OWNER TO postgres;

--
-- Name: user_games_game_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_games_game_id_seq OWNED BY public.user_games.game_id;


--
-- Name: user_games_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_games_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_games_user_id_seq OWNER TO postgres;

--
-- Name: user_games_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_games_user_id_seq OWNED BY public.user_games.user_id;


--
-- Name: user_orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_orders (
    user_id integer NOT NULL,
    game_id integer NOT NULL,
    product_id integer NOT NULL,
    total_price numeric,
    quantity integer,
    transaction_type public.transactiontype,
    transaction_date date
);


ALTER TABLE public.user_orders OWNER TO postgres;

--
-- Name: user_orders_game_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_orders_game_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_orders_game_id_seq OWNER TO postgres;

--
-- Name: user_orders_game_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_orders_game_id_seq OWNED BY public.user_orders.game_id;


--
-- Name: user_orders_product_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_orders_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_orders_product_id_seq OWNER TO postgres;

--
-- Name: user_orders_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_orders_product_id_seq OWNED BY public.user_orders.product_id;


--
-- Name: user_orders_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_orders_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_orders_user_id_seq OWNER TO postgres;

--
-- Name: user_orders_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_orders_user_id_seq OWNED BY public.user_orders.user_id;


--
-- Name: user_tickets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_tickets (
    user_id integer NOT NULL,
    ticket_type public.tickettype,
    message text,
    created_at date
);


ALTER TABLE public.user_tickets OWNER TO postgres;

--
-- Name: user_tickets_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_tickets_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_tickets_user_id_seq OWNER TO postgres;

--
-- Name: user_tickets_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_tickets_user_id_seq OWNED BY public.user_tickets.user_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    name character varying(255),
    email character varying(255),
    password character varying(64),
    is_active boolean DEFAULT false,
    is_validated boolean DEFAULT false
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: available_games game_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.available_games ALTER COLUMN game_id SET DEFAULT nextval('public.available_games_game_id_seq'::regclass);


--
-- Name: ingame_products product_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingame_products ALTER COLUMN product_id SET DEFAULT nextval('public.ingame_products_product_id_seq'::regclass);


--
-- Name: ingame_products game_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingame_products ALTER COLUMN game_id SET DEFAULT nextval('public.ingame_products_game_id_seq'::regclass);


--
-- Name: user_games user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_games ALTER COLUMN user_id SET DEFAULT nextval('public.user_games_user_id_seq'::regclass);


--
-- Name: user_games game_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_games ALTER COLUMN game_id SET DEFAULT nextval('public.user_games_game_id_seq'::regclass);


--
-- Name: user_orders user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_orders ALTER COLUMN user_id SET DEFAULT nextval('public.user_orders_user_id_seq'::regclass);


--
-- Name: user_orders game_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_orders ALTER COLUMN game_id SET DEFAULT nextval('public.user_orders_game_id_seq'::regclass);


--
-- Name: user_orders product_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_orders ALTER COLUMN product_id SET DEFAULT nextval('public.user_orders_product_id_seq'::regclass);


--
-- Name: user_tickets user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_tickets ALTER COLUMN user_id SET DEFAULT nextval('public.user_tickets_user_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: available_games; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.available_games (game_id, title, description, is_active) FROM stdin;
1	Droid Shooter	Droid Shooter is a first of it's kind global multiplayer demo game that shows off all the features of Google Cloud for Games.	t
2	Cloud Royale	A brand new title in battle royale style that shows capabilities of massive scale and integration of Generative AI features into gaming mechanics.	t
\.


--
-- Data for Name: ingame_products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ingame_products (product_id, game_id, title, description, price, is_active) FROM stdin;
2	2	Cloud Gold	Gold for in-game trading	1.1	t
1	1	Cloud Gem	Gems for in-game purchases	1	t
\.


--
-- Data for Name: user_games; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_games (user_id, game_id, purchase_date, time_played) FROM stdin;
1	1	2024-04-18	1
\.


--
-- Data for Name: user_orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_orders (user_id, game_id, product_id, total_price, quantity, transaction_type, transaction_date) FROM stdin;
1	1	2	110	10	purchase	2024-04-19
1	1	1	30	3	purchase	2024-04-19
\.


--
-- Data for Name: user_tickets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_tickets (user_id, ticket_type, message, created_at) FROM stdin;
1	general	Just wanted to ask you about any other upcoming games. Thank you!	2024-04-19
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, name, email, password, is_active, is_validated) FROM stdin;
1	Nikolai	nikolaidan@google.com	b0aeb4c74df3cd681b9565e769967c2ec46c80da63bfe5165bd4b46ccb309c38	t	t
2	Nonna	nonna@google.com	b0aeb4c74df3cd681b9565e769967c2ec46c80da63bfe5165bd4b46ccb309c38	t	t
\.


--
-- Name: available_games_game_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.available_games_game_id_seq', 1, false);


--
-- Name: ingame_products_game_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ingame_products_game_id_seq', 1, false);


--
-- Name: ingame_products_product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ingame_products_product_id_seq', 1, false);


--
-- Name: user_games_game_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_games_game_id_seq', 1, false);


--
-- Name: user_games_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_games_user_id_seq', 1, false);


--
-- Name: user_orders_game_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_orders_game_id_seq', 1, false);


--
-- Name: user_orders_product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_orders_product_id_seq', 1, false);


--
-- Name: user_orders_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_orders_user_id_seq', 1, false);


--
-- Name: user_tickets_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_tickets_user_id_seq', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, false);


--
-- Name: available_games available_games_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.available_games
    ADD CONSTRAINT available_games_pkey PRIMARY KEY (game_id);


--
-- Name: ingame_products ingame_products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingame_products
    ADD CONSTRAINT ingame_products_pkey PRIMARY KEY (product_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: ingame_products ingame_products_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingame_products
    ADD CONSTRAINT ingame_products_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.available_games(game_id);


--
-- Name: user_games user_games_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_games
    ADD CONSTRAINT user_games_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.available_games(game_id);


--
-- Name: user_games user_games_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_games
    ADD CONSTRAINT user_games_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: user_orders user_orders_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_orders
    ADD CONSTRAINT user_orders_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.available_games(game_id);


--
-- Name: user_orders user_orders_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_orders
    ADD CONSTRAINT user_orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: user_tickets user_tickets_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_tickets
    ADD CONSTRAINT user_tickets_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--
