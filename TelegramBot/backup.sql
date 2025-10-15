--
-- PostgreSQL database dump
--

\restrict e8wlhsbnYHelEIT0Yq9sGhaOkbRpiCprGFDH4rVqq3Is0Prqn1DBcGN0UNsInwf

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: actions_tbl; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.actions_tbl (
    "time" time(6) without time zone,
    type smallint,
    id_tg_user bigint NOT NULL,
    CONSTRAINT actions_tbl_type_check CHECK (((type >= 0) AND (type <= 1)))
);


ALTER TABLE public.actions_tbl OWNER TO postgres;

--
-- Name: current_date_tbl; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.current_date_tbl (
    "boolean" boolean,
    type smallint,
    id_tg_user bigint NOT NULL,
    CONSTRAINT current_date_tbl_type_check CHECK (((type >= 0) AND (type <= 1)))
);


ALTER TABLE public.current_date_tbl OWNER TO postgres;

--
-- Name: indicators_for_day; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.indicators_for_day (
    name_value smallint,
    "time" time(6) without time zone,
    value integer,
    id_tg_user bigint NOT NULL,
    CONSTRAINT indicators_for_day_name_value_check CHECK (((name_value >= 0) AND (name_value <= 1)))
);


ALTER TABLE public.indicators_for_day OWNER TO postgres;

--
-- Name: notifications_tbl; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notifications_tbl (
    name_value smallint,
    value integer,
    id_tg_user bigint NOT NULL,
    CONSTRAINT notifications_tbl_name_value_check CHECK (((name_value >= 0) AND (name_value <= 1)))
);


ALTER TABLE public.notifications_tbl OWNER TO postgres;

--
-- Name: recommendations_tbl; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.recommendations_tbl (
    date date,
    text character varying(255),
    id_tg_user bigint NOT NULL
);


ALTER TABLE public.recommendations_tbl OWNER TO postgres;

--
-- Name: users_tbl; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users_tbl (
    id_tg_user bigint NOT NULL,
    ip_greenhouse character varying(255),
    id_token_greenhouse character varying(255)
);


ALTER TABLE public.users_tbl OWNER TO postgres;

--
-- Data for Name: actions_tbl; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.actions_tbl ("time", type, id_tg_user) FROM stdin;
\.


--
-- Data for Name: current_date_tbl; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.current_date_tbl ("boolean", type, id_tg_user) FROM stdin;
\.


--
-- Data for Name: indicators_for_day; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.indicators_for_day (name_value, "time", value, id_tg_user) FROM stdin;
\.


--
-- Data for Name: notifications_tbl; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notifications_tbl (name_value, value, id_tg_user) FROM stdin;
\.


--
-- Data for Name: recommendations_tbl; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.recommendations_tbl (date, text, id_tg_user) FROM stdin;
\.


--
-- Data for Name: users_tbl; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users_tbl (id_tg_user, ip_greenhouse, id_token_greenhouse) FROM stdin;
\.


--
-- Name: actions_tbl actions_tbl_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actions_tbl
    ADD CONSTRAINT actions_tbl_pkey PRIMARY KEY (id_tg_user);


--
-- Name: current_date_tbl current_date_tbl_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.current_date_tbl
    ADD CONSTRAINT current_date_tbl_pkey PRIMARY KEY (id_tg_user);


--
-- Name: indicators_for_day indicators_for_day_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.indicators_for_day
    ADD CONSTRAINT indicators_for_day_pkey PRIMARY KEY (id_tg_user);


--
-- Name: notifications_tbl notifications_tbl_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications_tbl
    ADD CONSTRAINT notifications_tbl_pkey PRIMARY KEY (id_tg_user);


--
-- Name: recommendations_tbl recommendations_tbl_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recommendations_tbl
    ADD CONSTRAINT recommendations_tbl_pkey PRIMARY KEY (id_tg_user);


--
-- Name: users_tbl users_tbl_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_tbl
    ADD CONSTRAINT users_tbl_pkey PRIMARY KEY (id_tg_user);


--
-- Name: actions_tbl fkb1uf0vb2dl3yq3q9pvu0owm6u; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actions_tbl
    ADD CONSTRAINT fkb1uf0vb2dl3yq3q9pvu0owm6u FOREIGN KEY (id_tg_user) REFERENCES public.users_tbl(id_tg_user);


--
-- Name: current_date_tbl fkg1s9icxjhhlh201n4m5ok9dls; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.current_date_tbl
    ADD CONSTRAINT fkg1s9icxjhhlh201n4m5ok9dls FOREIGN KEY (id_tg_user) REFERENCES public.users_tbl(id_tg_user);


--
-- Name: indicators_for_day fkgoyx2hpw64xkshc168botucm7; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.indicators_for_day
    ADD CONSTRAINT fkgoyx2hpw64xkshc168botucm7 FOREIGN KEY (id_tg_user) REFERENCES public.users_tbl(id_tg_user);


--
-- Name: notifications_tbl fkn7nq47n16x10clcdurkcfs92x; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications_tbl
    ADD CONSTRAINT fkn7nq47n16x10clcdurkcfs92x FOREIGN KEY (id_tg_user) REFERENCES public.users_tbl(id_tg_user);


--
-- Name: recommendations_tbl fkrcu8mvuyhsjqa69usti004t3h; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recommendations_tbl
    ADD CONSTRAINT fkrcu8mvuyhsjqa69usti004t3h FOREIGN KEY (id_tg_user) REFERENCES public.users_tbl(id_tg_user);


--
-- PostgreSQL database dump complete
--

\unrestrict e8wlhsbnYHelEIT0Yq9sGhaOkbRpiCprGFDH4rVqq3Is0Prqn1DBcGN0UNsInwf

