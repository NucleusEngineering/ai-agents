--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2 (Debian 16.2-1.pgdg120+2)
-- Dumped by pg_dump version 16.2

-- Started on 2024-04-19 10:33:19

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
-- TOC entry 858 (class 1247 OID 16396)
-- Name: tickettype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.tickettype AS ENUM (
    'general',
    'billing',
    'account'
);


ALTER TYPE public.tickettype OWNER TO postgres;

--
-- TOC entry 855 (class 1247 OID 16390)
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
-- TOC entry 218 (class 1259 OID 16415)
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
-- TOC entry 217 (class 1259 OID 16414)
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
-- TOC entry 3426 (class 0 OID 0)
-- Dependencies: 217
-- Name: available_games_game_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.available_games_game_id_seq OWNED BY public.available_games.game_id;


--
-- TOC entry 221 (class 1259 OID 16425)
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
-- TOC entry 220 (class 1259 OID 16424)
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
-- TOC entry 3427 (class 0 OID 0)
-- Dependencies: 220
-- Name: ingame_products_game_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ingame_products_game_id_seq OWNED BY public.ingame_products.game_id;


--
-- TOC entry 219 (class 1259 OID 16423)
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
-- TOC entry 3428 (class 0 OID 0)
-- Dependencies: 219
-- Name: ingame_products_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ingame_products_product_id_seq OWNED BY public.ingame_products.product_id;


--
-- TOC entry 228 (class 1259 OID 16462)
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
-- TOC entry 227 (class 1259 OID 16461)
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
-- TOC entry 3429 (class 0 OID 0)
-- Dependencies: 227
-- Name: user_games_game_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_games_game_id_seq OWNED BY public.user_games.game_id;


--
-- TOC entry 226 (class 1259 OID 16460)
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
-- TOC entry 3430 (class 0 OID 0)
-- Dependencies: 226
-- Name: user_games_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_games_user_id_seq OWNED BY public.user_games.user_id;


--
-- TOC entry 225 (class 1259 OID 16442)
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
-- TOC entry 223 (class 1259 OID 16440)
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
-- TOC entry 3431 (class 0 OID 0)
-- Dependencies: 223
-- Name: user_orders_game_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_orders_game_id_seq OWNED BY public.user_orders.game_id;


--
-- TOC entry 224 (class 1259 OID 16441)
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
-- TOC entry 3432 (class 0 OID 0)
-- Dependencies: 224
-- Name: user_orders_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_orders_product_id_seq OWNED BY public.user_orders.product_id;


--
-- TOC entry 222 (class 1259 OID 16439)
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
-- TOC entry 3433 (class 0 OID 0)
-- Dependencies: 222
-- Name: user_orders_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_orders_user_id_seq OWNED BY public.user_orders.user_id;


--
-- TOC entry 230 (class 1259 OID 16478)
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
-- TOC entry 229 (class 1259 OID 16477)
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
-- TOC entry 3434 (class 0 OID 0)
-- Dependencies: 229
-- Name: user_tickets_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_tickets_user_id_seq OWNED BY public.user_tickets.user_id;


--
-- TOC entry 216 (class 1259 OID 16404)
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
-- TOC entry 215 (class 1259 OID 16403)
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
-- TOC entry 3435 (class 0 OID 0)
-- Dependencies: 215
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- TOC entry 3241 (class 2604 OID 16418)
-- Name: available_games game_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.available_games ALTER COLUMN game_id SET DEFAULT nextval('public.available_games_game_id_seq'::regclass);


--
-- TOC entry 3242 (class 2604 OID 16428)
-- Name: ingame_products product_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingame_products ALTER COLUMN product_id SET DEFAULT nextval('public.ingame_products_product_id_seq'::regclass);


--
-- TOC entry 3243 (class 2604 OID 16429)
-- Name: ingame_products game_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingame_products ALTER COLUMN game_id SET DEFAULT nextval('public.ingame_products_game_id_seq'::regclass);


--
-- TOC entry 3247 (class 2604 OID 16465)
-- Name: user_games user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_games ALTER COLUMN user_id SET DEFAULT nextval('public.user_games_user_id_seq'::regclass);


--
-- TOC entry 3248 (class 2604 OID 16466)
-- Name: user_games game_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_games ALTER COLUMN game_id SET DEFAULT nextval('public.user_games_game_id_seq'::regclass);


--
-- TOC entry 3244 (class 2604 OID 16445)
-- Name: user_orders user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_orders ALTER COLUMN user_id SET DEFAULT nextval('public.user_orders_user_id_seq'::regclass);


--
-- TOC entry 3245 (class 2604 OID 16446)
-- Name: user_orders game_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_orders ALTER COLUMN game_id SET DEFAULT nextval('public.user_orders_game_id_seq'::regclass);


--
-- TOC entry 3246 (class 2604 OID 16447)
-- Name: user_orders product_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_orders ALTER COLUMN product_id SET DEFAULT nextval('public.user_orders_product_id_seq'::regclass);


--
-- TOC entry 3249 (class 2604 OID 16481)
-- Name: user_tickets user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_tickets ALTER COLUMN user_id SET DEFAULT nextval('public.user_tickets_user_id_seq'::regclass);


--
-- TOC entry 3238 (class 2604 OID 16407)
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- TOC entry 3408 (class 0 OID 16415)
-- Dependencies: 218
-- Data for Name: available_games; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.available_games (game_id, title, description, is_active) FROM stdin;
1	Droid Shooter	Droid Shooter is a first of it's kind global multiplayer demo game that shows off all the features of Google Cloud for Games.	t
2	Cloud Royale	A brand new title in battle royale style that shows capabilities of massive scale and integration of Generative AI features into gaming mechanics.	t
\.


--
-- TOC entry 3411 (class 0 OID 16425)
-- Dependencies: 221
-- Data for Name: ingame_products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ingame_products (product_id, game_id, title, description, price, is_active) FROM stdin;
2	2	Cloud Gold	Gold for in-game trading	1.1	t
1	1	Cloud Gem	Gems for in-game purchases	1	t
\.


--
-- TOC entry 3418 (class 0 OID 16462)
-- Dependencies: 228
-- Data for Name: user_games; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_games (user_id, game_id, purchase_date, time_played) FROM stdin;
1	1	2024-04-18	1
\.


--
-- TOC entry 3415 (class 0 OID 16442)
-- Dependencies: 225
-- Data for Name: user_orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_orders (user_id, game_id, product_id, total_price, quantity, transaction_type, transaction_date) FROM stdin;
\.


--
-- TOC entry 3420 (class 0 OID 16478)
-- Dependencies: 230
-- Data for Name: user_tickets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_tickets (user_id, ticket_type, message, created_at) FROM stdin;
\.


--
-- TOC entry 3406 (class 0 OID 16404)
-- Dependencies: 216
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, name, email, password, is_active, is_validated) FROM stdin;
1	Nikolai	nikolaidan@google.com	b0aeb4c74df3cd681b9565e769967c2ec46c80da63bfe5165bd4b46ccb309c38	t	t
\.


--
-- TOC entry 3436 (class 0 OID 0)
-- Dependencies: 217
-- Name: available_games_game_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.available_games_game_id_seq', 1, false);


--
-- TOC entry 3437 (class 0 OID 0)
-- Dependencies: 220
-- Name: ingame_products_game_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ingame_products_game_id_seq', 1, false);


--
-- TOC entry 3438 (class 0 OID 0)
-- Dependencies: 219
-- Name: ingame_products_product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ingame_products_product_id_seq', 1, false);


--
-- TOC entry 3439 (class 0 OID 0)
-- Dependencies: 227
-- Name: user_games_game_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_games_game_id_seq', 1, false);


--
-- TOC entry 3440 (class 0 OID 0)
-- Dependencies: 226
-- Name: user_games_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_games_user_id_seq', 1, false);


--
-- TOC entry 3441 (class 0 OID 0)
-- Dependencies: 223
-- Name: user_orders_game_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_orders_game_id_seq', 1, false);


--
-- TOC entry 3442 (class 0 OID 0)
-- Dependencies: 224
-- Name: user_orders_product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_orders_product_id_seq', 1, false);


--
-- TOC entry 3443 (class 0 OID 0)
-- Dependencies: 222
-- Name: user_orders_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_orders_user_id_seq', 1, false);


--
-- TOC entry 3444 (class 0 OID 0)
-- Dependencies: 229
-- Name: user_tickets_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_tickets_user_id_seq', 1, false);


--
-- TOC entry 3445 (class 0 OID 0)
-- Dependencies: 215
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, false);


--
-- TOC entry 3253 (class 2606 OID 16422)
-- Name: available_games available_games_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.available_games
    ADD CONSTRAINT available_games_pkey PRIMARY KEY (game_id);


--
-- TOC entry 3255 (class 2606 OID 16433)
-- Name: ingame_products ingame_products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingame_products
    ADD CONSTRAINT ingame_products_pkey PRIMARY KEY (product_id);


--
-- TOC entry 3251 (class 2606 OID 16413)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- TOC entry 3256 (class 2606 OID 16434)
-- Name: ingame_products ingame_products_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ingame_products
    ADD CONSTRAINT ingame_products_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.available_games(game_id);


--
-- TOC entry 3259 (class 2606 OID 16472)
-- Name: user_games user_games_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_games
    ADD CONSTRAINT user_games_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.available_games(game_id);


--
-- TOC entry 3260 (class 2606 OID 16467)
-- Name: user_games user_games_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_games
    ADD CONSTRAINT user_games_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- TOC entry 3257 (class 2606 OID 16455)
-- Name: user_orders user_orders_game_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_orders
    ADD CONSTRAINT user_orders_game_id_fkey FOREIGN KEY (game_id) REFERENCES public.available_games(game_id);


--
-- TOC entry 3258 (class 2606 OID 16450)
-- Name: user_orders user_orders_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_orders
    ADD CONSTRAINT user_orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- TOC entry 3261 (class 2606 OID 16484)
-- Name: user_tickets user_tickets_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_tickets
    ADD CONSTRAINT user_tickets_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


-- Completed on 2024-04-19 10:33:20

--
-- PostgreSQL database dump complete
--

