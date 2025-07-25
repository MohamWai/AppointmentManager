--
-- PostgreSQL database dump
--

-- Dumped from database version 14.18 (Homebrew)
-- Dumped by pg_dump version 14.18 (Homebrew)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: appointments; Type: TABLE; Schema: public; Owner: clinicuser
--

CREATE TABLE public.appointments (
    id integer NOT NULL,
    patient_id integer NOT NULL,
    doctor_id integer NOT NULL,
    date date,
    "time" time without time zone,
    duration integer,
    reason text,
    status character varying,
    package_id integer,
    appointment_type character varying
);


ALTER TABLE public.appointments OWNER TO clinicuser;

--
-- Name: appointments_id_seq; Type: SEQUENCE; Schema: public; Owner: clinicuser
--

CREATE SEQUENCE public.appointments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.appointments_id_seq OWNER TO clinicuser;

--
-- Name: appointments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: clinicuser
--

ALTER SEQUENCE public.appointments_id_seq OWNED BY public.appointments.id;


--
-- Name: doctors; Type: TABLE; Schema: public; Owner: clinicuser
--

CREATE TABLE public.doctors (
    id integer NOT NULL,
    name character varying NOT NULL,
    specialty character varying,
    phone character varying,
    email character varying,
    status character varying
);


ALTER TABLE public.doctors OWNER TO clinicuser;

--
-- Name: doctors_id_seq; Type: SEQUENCE; Schema: public; Owner: clinicuser
--

CREATE SEQUENCE public.doctors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.doctors_id_seq OWNER TO clinicuser;

--
-- Name: doctors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: clinicuser
--

ALTER SEQUENCE public.doctors_id_seq OWNED BY public.doctors.id;


--
-- Name: notes; Type: TABLE; Schema: public; Owner: clinicuser
--

CREATE TABLE public.notes (
    id integer NOT NULL,
    appointment_id integer NOT NULL,
    doctor_id integer NOT NULL,
    patient_id integer NOT NULL,
    note_type character varying,
    content text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.notes OWNER TO clinicuser;

--
-- Name: notes_id_seq; Type: SEQUENCE; Schema: public; Owner: clinicuser
--

CREATE SEQUENCE public.notes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.notes_id_seq OWNER TO clinicuser;

--
-- Name: notes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: clinicuser
--

ALTER SEQUENCE public.notes_id_seq OWNED BY public.notes.id;


--
-- Name: packages; Type: TABLE; Schema: public; Owner: clinicuser
--

CREATE TABLE public.packages (
    id integer NOT NULL,
    patient_id integer NOT NULL,
    start_date date,
    weekdays character varying,
    total_sessions integer,
    status character varying
);


ALTER TABLE public.packages OWNER TO clinicuser;

--
-- Name: packages_id_seq; Type: SEQUENCE; Schema: public; Owner: clinicuser
--

CREATE SEQUENCE public.packages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.packages_id_seq OWNER TO clinicuser;

--
-- Name: packages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: clinicuser
--

ALTER SEQUENCE public.packages_id_seq OWNED BY public.packages.id;


--
-- Name: patients; Type: TABLE; Schema: public; Owner: clinicuser
--

CREATE TABLE public.patients (
    id integer NOT NULL,
    name character varying NOT NULL,
    phone character varying NOT NULL,
    gender character varying
);


ALTER TABLE public.patients OWNER TO clinicuser;

--
-- Name: patients_id_seq; Type: SEQUENCE; Schema: public; Owner: clinicuser
--

CREATE SEQUENCE public.patients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.patients_id_seq OWNER TO clinicuser;

--
-- Name: patients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: clinicuser
--

ALTER SEQUENCE public.patients_id_seq OWNED BY public.patients.id;


--
-- Name: appointments id; Type: DEFAULT; Schema: public; Owner: clinicuser
--

ALTER TABLE ONLY public.appointments ALTER COLUMN id SET DEFAULT nextval('public.appointments_id_seq'::regclass);


--
-- Name: doctors id; Type: DEFAULT; Schema: public; Owner: clinicuser
--

ALTER TABLE ONLY public.doctors ALTER COLUMN id SET DEFAULT nextval('public.doctors_id_seq'::regclass);


--
-- Name: notes id; Type: DEFAULT; Schema: public; Owner: clinicuser
--

ALTER TABLE ONLY public.notes ALTER COLUMN id SET DEFAULT nextval('public.notes_id_seq'::regclass);


--
-- Name: packages id; Type: DEFAULT; Schema: public; Owner: clinicuser
--

ALTER TABLE ONLY public.packages ALTER COLUMN id SET DEFAULT nextval('public.packages_id_seq'::regclass);


--
-- Name: patients id; Type: DEFAULT; Schema: public; Owner: clinicuser
--

ALTER TABLE ONLY public.patients ALTER COLUMN id SET DEFAULT nextval('public.patients_id_seq'::regclass);


--
-- Data for Name: appointments; Type: TABLE DATA; Schema: public; Owner: clinicuser
--

COPY public.appointments (id, patient_id, doctor_id, date, "time", duration, reason, status, package_id, appointment_type) FROM stdin;
\.


--
-- Data for Name: doctors; Type: TABLE DATA; Schema: public; Owner: clinicuser
--

COPY public.doctors (id, name, specialty, phone, email, status) FROM stdin;
\.


--
-- Data for Name: notes; Type: TABLE DATA; Schema: public; Owner: clinicuser
--

COPY public.notes (id, appointment_id, doctor_id, patient_id, note_type, content, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: packages; Type: TABLE DATA; Schema: public; Owner: clinicuser
--

COPY public.packages (id, patient_id, start_date, weekdays, total_sessions, status) FROM stdin;
\.


--
-- Data for Name: patients; Type: TABLE DATA; Schema: public; Owner: clinicuser
--

COPY public.patients (id, name, phone, gender) FROM stdin;
1	osama	92027456	Male
\.


--
-- Name: appointments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: clinicuser
--

SELECT pg_catalog.setval('public.appointments_id_seq', 1, false);


--
-- Name: doctors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: clinicuser
--

SELECT pg_catalog.setval('public.doctors_id_seq', 1, false);


--
-- Name: notes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: clinicuser
--

SELECT pg_catalog.setval('public.notes_id_seq', 1, false);


--
-- Name: packages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: clinicuser
--

SELECT pg_catalog.setval('public.packages_id_seq', 1, false);


--
-- Name: patients_id_seq; Type: SEQUENCE SET; Schema: public; Owner: clinicuser
--

SELECT pg_catalog.setval('public.patients_id_seq', 1, true);


--
-- Name: appointments appointments_pkey; Type: CONSTRAINT; Schema: public; Owner: clinicuser
--

ALTER TABLE ONLY public.appointments
    ADD CONSTRAINT appointments_pkey PRIMARY KEY (id);


--
-- Name: doctors doctors_pkey; Type: CONSTRAINT; Schema: public; Owner: clinicuser
--

ALTER TABLE ONLY public.doctors
    ADD CONSTRAINT doctors_pkey PRIMARY KEY (id);


--
-- Name: notes notes_pkey; Type: CONSTRAINT; Schema: public; Owner: clinicuser
--

ALTER TABLE ONLY public.notes
    ADD CONSTRAINT notes_pkey PRIMARY KEY (id);


--
-- Name: packages packages_pkey; Type: CONSTRAINT; Schema: public; Owner: clinicuser
--

ALTER TABLE ONLY public.packages
    ADD CONSTRAINT packages_pkey PRIMARY KEY (id);


--
-- Name: patients patients_phone_key; Type: CONSTRAINT; Schema: public; Owner: clinicuser
--

ALTER TABLE ONLY public.patients
    ADD CONSTRAINT patients_phone_key UNIQUE (phone);


--
-- Name: patients patients_pkey; Type: CONSTRAINT; Schema: public; Owner: clinicuser
--

ALTER TABLE ONLY public.patients
    ADD CONSTRAINT patients_pkey PRIMARY KEY (id);


--
-- Name: appointments appointments_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clinicuser
--

ALTER TABLE ONLY public.appointments
    ADD CONSTRAINT appointments_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctors(id);


--
-- Name: appointments appointments_package_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clinicuser
--

ALTER TABLE ONLY public.appointments
    ADD CONSTRAINT appointments_package_id_fkey FOREIGN KEY (package_id) REFERENCES public.packages(id);


--
-- Name: appointments appointments_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clinicuser
--

ALTER TABLE ONLY public.appointments
    ADD CONSTRAINT appointments_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: notes notes_appointment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clinicuser
--

ALTER TABLE ONLY public.notes
    ADD CONSTRAINT notes_appointment_id_fkey FOREIGN KEY (appointment_id) REFERENCES public.appointments(id) ON DELETE CASCADE;


--
-- Name: notes notes_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clinicuser
--

ALTER TABLE ONLY public.notes
    ADD CONSTRAINT notes_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctors(id);


--
-- Name: notes notes_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clinicuser
--

ALTER TABLE ONLY public.notes
    ADD CONSTRAINT notes_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- Name: packages packages_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: clinicuser
--

ALTER TABLE ONLY public.packages
    ADD CONSTRAINT packages_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id);


--
-- PostgreSQL database dump complete
--

