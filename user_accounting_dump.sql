--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.6
-- Dumped by pg_dump version 9.6.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: DATABASE user_accounting; Type: MAC LABEL; Schema: -; Owner: postgres
--

MAC LABEL ON DATABASE CURRENT_CATALOG IS '{0,0}';


--
-- Name: DATABASE user_accounting; Type: MAC CCR; Schema: -; Owner: postgres
--

MAC CCR ON DATABASE CURRENT_CATALOG IS ON;


--
-- Name: SCHEMA public; Type: MAC LABEL; Schema: -; Owner: postgres
--

MAC LABEL ON SCHEMA public IS '{0,0}';


--
-- Name: SCHEMA public; Type: MAC CCR; Schema: -; Owner: postgres
--

MAC CCR ON SCHEMA public IS ON;


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = pg_catalog;

--
-- Name: EXTENSION plpgsql; Type: MAC LABEL; Schema: pg_catalog; Owner: 
--

MAC LABEL ON EXTENSION plpgsql IS '{0,0}';


--
-- Name: LANGUAGE plpgsql; Type: MAC LABEL; Schema: -; Owner: 
--

MAC LABEL ON LANGUAGE plpgsql IS '{0,0}';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: audit_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE audit_log (
    id integer NOT NULL,
    admin_login character varying(50),
    action character varying(100),
    target_login character varying(50),
    created_at timestamp without time zone DEFAULT now()
)
WITH (MACS=FALSE);


ALTER TABLE audit_log OWNER TO postgres;

--
-- Name: TABLE audit_log; Type: MAC LABEL; Schema: public; Owner: postgres
--

MAC LABEL ON TABLE audit_log IS '{0,0}';


--
-- Name: TABLE audit_log; Type: MAC CCR; Schema: public; Owner: postgres
--

MAC CCR ON TABLE audit_log IS ON;


--
-- Name: audit_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE audit_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE audit_log_id_seq OWNER TO postgres;

--
-- Name: audit_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE audit_log_id_seq OWNED BY audit_log.id;


--
-- Name: SEQUENCE audit_log_id_seq; Type: MAC LABEL; Schema: public; Owner: postgres
--

MAC LABEL ON SEQUENCE audit_log_id_seq IS '{0,0}';


--
-- Name: SEQUENCE audit_log_id_seq; Type: MAC CCR; Schema: public; Owner: postgres
--

MAC CCR ON SEQUENCE audit_log_id_seq IS ON;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE users (
    id integer NOT NULL,
    login character varying(50) NOT NULL,
    password_hash character varying(64) NOT NULL,
    full_name character varying(100),
    "position" character varying(50),
    phone character varying(20),
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT now(),
    role character varying(20) DEFAULT 'user'::character varying
)
WITH (MACS=FALSE);


ALTER TABLE users OWNER TO postgres;

--
-- Name: TABLE users; Type: MAC LABEL; Schema: public; Owner: postgres
--

MAC LABEL ON TABLE users IS '{0,0}';


--
-- Name: TABLE users; Type: MAC CCR; Schema: public; Owner: postgres
--

MAC CCR ON TABLE users IS ON;


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: SEQUENCE users_id_seq; Type: MAC LABEL; Schema: public; Owner: postgres
--

MAC LABEL ON SEQUENCE users_id_seq IS '{0,0}';


--
-- Name: SEQUENCE users_id_seq; Type: MAC CCR; Schema: public; Owner: postgres
--

MAC CCR ON SEQUENCE users_id_seq IS ON;


--
-- Name: audit_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY audit_log ALTER COLUMN id SET DEFAULT nextval('audit_log_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Data for Name: audit_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY audit_log (id, admin_login, action, target_login, created_at) FROM stdin;
1	admin	create_user	shegoleva	2026-07-12 02:37:41.615529
2	admin	update_user	shegoleva	2026-07-12 04:11:46.869172
3	admin	update_user	shegoleva	2026-07-12 06:18:22.309969
4	admin	create_user	Filonov	2026-07-12 08:14:49.455273
5	admin	create_user	Dorofeeva	2026-07-12 09:45:01.410413
6	admin	update_user	shegoleva	2026-07-12 16:30:31.24688
7	admin	create_user	Orekhova	2026-07-12 18:24:40.128149
8	admin	update_user	shegoleva	2026-07-12 18:24:49.385809
9	admin	create_user	Kyznetsov	2026-07-12 18:26:12.693834
10	admin	create_user	Urov	2026-07-12 18:27:06.480076
11	admin	create_user	Kolomytseva	2026-07-12 18:29:10.45426
12	admin	create_user	Shegusov	2026-07-12 18:30:55.621695
13	admin	create_user	Filimonova	2026-07-12 18:31:58.717512
14	admin	create_user	Kalashnikova	2026-07-12 18:33:26.248109
15	admin	delete_user	Kalashnikova	2026-07-14 02:44:16.793281
16	admin	create_user	vertman	2026-07-14 03:16:40.909045
17	admin	update_user	vertman	2026-07-14 03:16:55.892547
\.


-- Obtained maclabel {0,0}
--
-- Name: audit_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('audit_log_id_seq', 17, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY users (id, login, password_hash, full_name, "position", phone, is_active, created_at, role) FROM stdin;
1	admin	8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918	Главный Администратор	Администратор	+7 900 000 00 00	t	2026-07-12 02:25:13.098004	admin
3	Filonov	6c84b1086e558a0b9dad7623979f6ddf9f337084f281d9b3a07273d04b425344	Филонов Иван Андреевич	Менеджер	+7 920 746 98 45	t	2026-07-12 08:14:49.421391	user
4	Dorofeeva	caf7f390e9f40e2c066edd63ea28220420f7d62e06a60d3d31ef410ec48098bd	Дорофеева Софья Евгеньевна	Разработчик	+7 951 599 94 67	t	2026-07-12 09:45:01.368182	user
5	Orekhova	3b6eadd8c9c691e2e6c5b2d853cf7776b47f83bf3fb57f7cf08ca36c3a972577	Орехова Валерия Сергеевна	Аналитик	+7 943 987 23 01	t	2026-07-12 18:24:40.094244	user
2	shegoleva	e1fc078b915708c37e1885b411a87e4bd318454a25a706360e3646ddbcaf085e	Щеголева Маргарита Юрьевна	Аналитик	+7 900 963 87 05	t	2026-07-12 02:37:41.57684	user
6	Kyznetsov	5f9524f95e61e01639d3bca1d4b8df4ac61b657409356f14c6dc566016ba3188	Кузнецов Дмитрий Васильевич	Тестировщик	+7 951 746 87 23	t	2026-07-12 18:26:12.668023	user
7	Urov	ac9a99e520345ce96e03157234f7f26a9a64e49dfd6d15a2e37d3f61252262c9	Юров Максим Валерьевич	Дизайнер	+7 964 567 83 64	t	2026-07-12 18:27:06.453978	user
8	Kolomytseva	a904ecf843164ec902ce38afc676a0ccac2c90c14ad76ab3e1fd8143b508f11a	Коломыцева Евгения Сергеевна	Менеджер	+7 976 456 45 23	t	2026-07-12 18:29:10.430239	user
9	Shegusov	ceb2ff42493dfcd1f3662362d28da4fc30f2d46cc12159f5aafe386aa9fb51fc	Шегусов Сергей Васильевич	Тестировщик	+7 987 467 98 67	t	2026-07-12 18:30:55.596336	admin
10	Filimonova	e5b5530a2611f74ad8d189ad2980897aec3bbecab15a3183dbb0e79031e7b467	Филимонова Яна Валерьевна	Дизайнер	+7 986 456 97 55	t	2026-07-12 18:31:58.679061	user
11	Kalashnikova	a5b6aebae097cb2dedf054905a82129dd833e8e48b11f289102c1ad0a34a139d	Калашникова Татьяна Владимировна	Аналитик	+7 876 998 34 77	f	2026-07-12 18:33:26.227642	user
12	vertman	9a7c4d9db1873b350c5a666b3da8a531f48fb41d255a68eacbc61d94640ff723	Вертман Ольга Алексеевна	Менеджер	+7 957 675 56 44	f	2026-07-14 03:16:40.871557	user
\.


-- Obtained maclabel {0,0}
--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('users_id_seq', 12, true);


--
-- Name: audit_log audit_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY audit_log
    ADD CONSTRAINT audit_log_pkey PRIMARY KEY (id);


--
-- Name: users users_login_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_login_key UNIQUE (login);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

