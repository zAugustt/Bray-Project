--
-- PostgreSQL database dump
--

-- Dumped from database version 13.19
-- Dumped by pg_dump version 17.2

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

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: bray_tamu
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO bray_tamu;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: device_datas; Type: TABLE; Schema: public; Owner: bray_tamu
--

CREATE TABLE public.device_datas (
    id integer NOT NULL,
    "lastTorqueBeforeSleep" integer NOT NULL,
    "firstTorqueAfterSleep" integer NOT NULL,
    "recordNumbers" integer[] NOT NULL,
    "recordLengths" integer[] NOT NULL,
    "torqueData" integer[] NOT NULL,
    "hiddenDataIndices" integer[] NOT NULL,
    "typeOfStroke" integer NOT NULL,
    "dataRecordPayloadCRCs" integer[] NOT NULL,
    "calculatedDataRecordPayloadCRCs" integer[] NOT NULL,
    "eventRecordPayloadCRC" integer NOT NULL,
    "calculatedEventRecordPayloadCRC" integer NOT NULL,
    "heartbeatRecordPayloadCRC" integer NOT NULL,
    "calculatedHeartbeatRecordPayloadCRC" integer NOT NULL
);


ALTER TABLE public.device_datas OWNER TO bray_tamu;

--
-- Name: device_datas_id_seq; Type: SEQUENCE; Schema: public; Owner: bray_tamu
--

CREATE SEQUENCE public.device_datas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.device_datas_id_seq OWNER TO bray_tamu;

--
-- Name: device_datas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bray_tamu
--

ALTER SEQUENCE public.device_datas_id_seq OWNED BY public.device_datas.id;


--
-- Name: device_infos; Type: TABLE; Schema: public; Owner: bray_tamu
--

CREATE TABLE public.device_infos (
    id integer NOT NULL,
    "firmwareVersion" character varying NOT NULL,
    "pwaRevision" character varying NOT NULL,
    "serialNumber" character varying NOT NULL,
    "deviceType" character varying NOT NULL,
    "deviceLocation" character varying NOT NULL,
    diagnostic integer NOT NULL,
    "openValveCount" integer NOT NULL,
    "closeValveCount" integer NOT NULL
);


ALTER TABLE public.device_infos OWNER TO bray_tamu;

--
-- Name: device_infos_id_seq; Type: SEQUENCE; Schema: public; Owner: bray_tamu
--

CREATE SEQUENCE public.device_infos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.device_infos_id_seq OWNER TO bray_tamu;

--
-- Name: device_infos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bray_tamu
--

ALTER SEQUENCE public.device_infos_id_seq OWNED BY public.device_infos.id;


--
-- Name: device_trend_infos; Type: TABLE; Schema: public; Owner: bray_tamu
--

CREATE TABLE public.device_trend_infos (
    id integer NOT NULL,
    "strokeTime" integer NOT NULL,
    "maxTorque" integer NOT NULL,
    temperature integer NOT NULL,
    "batteryVoltage" integer NOT NULL
);


ALTER TABLE public.device_trend_infos OWNER TO bray_tamu;

--
-- Name: device_trend_infos_id_seq; Type: SEQUENCE; Schema: public; Owner: bray_tamu
--

CREATE SEQUENCE public.device_trend_infos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.device_trend_infos_id_seq OWNER TO bray_tamu;

--
-- Name: device_trend_infos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bray_tamu
--

ALTER SEQUENCE public.device_trend_infos_id_seq OWNED BY public.device_trend_infos.id;


--
-- Name: events; Type: TABLE; Schema: public; Owner: bray_tamu
--

CREATE TABLE public.events (
    id integer NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    "isStreaming" boolean NOT NULL,
    "deviceInfoID" integer NOT NULL,
    "deviceDataID" integer NOT NULL,
    "deviceTrendInfoID" integer NOT NULL,
    "sensorID" integer NOT NULL
);


ALTER TABLE public.events OWNER TO bray_tamu;

--
-- Name: events_id_seq; Type: SEQUENCE; Schema: public; Owner: bray_tamu
--

CREATE SEQUENCE public.events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.events_id_seq OWNER TO bray_tamu;

--
-- Name: events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bray_tamu
--

ALTER SEQUENCE public.events_id_seq OWNED BY public.events.id;


--
-- Name: sensors; Type: TABLE; Schema: public; Owner: bray_tamu
--

CREATE TABLE public.sensors (
    id integer NOT NULL,
    "devEUI" character varying NOT NULL
);


ALTER TABLE public.sensors OWNER TO bray_tamu;

--
-- Name: sensors_id_seq; Type: SEQUENCE; Schema: public; Owner: bray_tamu
--

CREATE SEQUENCE public.sensors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sensors_id_seq OWNER TO bray_tamu;

--
-- Name: sensors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bray_tamu
--

ALTER SEQUENCE public.sensors_id_seq OWNED BY public.sensors.id;


--
-- Name: device_datas id; Type: DEFAULT; Schema: public; Owner: bray_tamu
--

ALTER TABLE ONLY public.device_datas ALTER COLUMN id SET DEFAULT nextval('public.device_datas_id_seq'::regclass);


--
-- Name: device_infos id; Type: DEFAULT; Schema: public; Owner: bray_tamu
--

ALTER TABLE ONLY public.device_infos ALTER COLUMN id SET DEFAULT nextval('public.device_infos_id_seq'::regclass);


--
-- Name: device_trend_infos id; Type: DEFAULT; Schema: public; Owner: bray_tamu
--

ALTER TABLE ONLY public.device_trend_infos ALTER COLUMN id SET DEFAULT nextval('public.device_trend_infos_id_seq'::regclass);


--
-- Name: events id; Type: DEFAULT; Schema: public; Owner: bray_tamu
--

ALTER TABLE ONLY public.events ALTER COLUMN id SET DEFAULT nextval('public.events_id_seq'::regclass);


--
-- Name: sensors id; Type: DEFAULT; Schema: public; Owner: bray_tamu
--

ALTER TABLE ONLY public.sensors ALTER COLUMN id SET DEFAULT nextval('public.sensors_id_seq'::regclass);


--
-- Data for Name: device_datas; Type: TABLE DATA; Schema: public; Owner: bray_tamu
--

COPY public.device_datas (id, "lastTorqueBeforeSleep", "firstTorqueAfterSleep", "recordNumbers", "recordLengths", "torqueData", "hiddenDataIndices", "typeOfStroke", "dataRecordPayloadCRCs", "calculatedDataRecordPayloadCRCs", "eventRecordPayloadCRC", "calculatedEventRecordPayloadCRC", "heartbeatRecordPayloadCRC", "calculatedHeartbeatRecordPayloadCRC") FROM stdin;
\.


--
-- Data for Name: device_infos; Type: TABLE DATA; Schema: public; Owner: bray_tamu
--

COPY public.device_infos (id, "firmwareVersion", "pwaRevision", "serialNumber", "deviceType", "deviceLocation", diagnostic, "openValveCount", "closeValveCount") FROM stdin;
\.


--
-- Data for Name: device_trend_infos; Type: TABLE DATA; Schema: public; Owner: bray_tamu
--

COPY public.device_trend_infos (id, "strokeTime", "maxTorque", temperature, "batteryVoltage") FROM stdin;
\.


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: bray_tamu
--

COPY public.events (id, "timestamp", "isStreaming", "deviceInfoID", "deviceDataID", "deviceTrendInfoID", "sensorID") FROM stdin;
\.


--
-- Data for Name: sensors; Type: TABLE DATA; Schema: public; Owner: bray_tamu
--

COPY public.sensors (id, "devEUI") FROM stdin;
\.


--
-- Name: device_datas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bray_tamu
--

SELECT pg_catalog.setval('public.device_datas_id_seq', 1, false);


--
-- Name: device_infos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bray_tamu
--

SELECT pg_catalog.setval('public.device_infos_id_seq', 1, false);


--
-- Name: device_trend_infos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bray_tamu
--

SELECT pg_catalog.setval('public.device_trend_infos_id_seq', 1, false);


--
-- Name: events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bray_tamu
--

SELECT pg_catalog.setval('public.events_id_seq', 1, false);


--
-- Name: sensors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bray_tamu
--

SELECT pg_catalog.setval('public.sensors_id_seq', 1, false);


--
-- Name: device_datas device_datas_pkey; Type: CONSTRAINT; Schema: public; Owner: bray_tamu
--

ALTER TABLE ONLY public.device_datas
    ADD CONSTRAINT device_datas_pkey PRIMARY KEY (id);


--
-- Name: device_infos device_infos_pkey; Type: CONSTRAINT; Schema: public; Owner: bray_tamu
--

ALTER TABLE ONLY public.device_infos
    ADD CONSTRAINT device_infos_pkey PRIMARY KEY (id);


--
-- Name: device_trend_infos device_trend_infos_pkey; Type: CONSTRAINT; Schema: public; Owner: bray_tamu
--

ALTER TABLE ONLY public.device_trend_infos
    ADD CONSTRAINT device_trend_infos_pkey PRIMARY KEY (id);


--
-- Name: events events_deviceDataID_key; Type: CONSTRAINT; Schema: public; Owner: bray_tamu
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT "events_deviceDataID_key" UNIQUE ("deviceDataID");


--
-- Name: events events_deviceInfoID_key; Type: CONSTRAINT; Schema: public; Owner: bray_tamu
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT "events_deviceInfoID_key" UNIQUE ("deviceInfoID");


--
-- Name: events events_deviceTrendInfoID_key; Type: CONSTRAINT; Schema: public; Owner: bray_tamu
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT "events_deviceTrendInfoID_key" UNIQUE ("deviceTrendInfoID");


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: bray_tamu
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (id);


--
-- Name: sensors sensors_devEUI_key; Type: CONSTRAINT; Schema: public; Owner: bray_tamu
--

ALTER TABLE ONLY public.sensors
    ADD CONSTRAINT "sensors_devEUI_key" UNIQUE ("devEUI");


--
-- Name: sensors sensors_pkey; Type: CONSTRAINT; Schema: public; Owner: bray_tamu
--

ALTER TABLE ONLY public.sensors
    ADD CONSTRAINT sensors_pkey PRIMARY KEY (id);


--
-- Name: events events_deviceDataID_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bray_tamu
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT "events_deviceDataID_fkey" FOREIGN KEY ("deviceDataID") REFERENCES public.device_datas(id);


--
-- Name: events events_deviceInfoID_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bray_tamu
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT "events_deviceInfoID_fkey" FOREIGN KEY ("deviceInfoID") REFERENCES public.device_infos(id);


--
-- Name: events events_deviceTrendInfoID_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bray_tamu
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT "events_deviceTrendInfoID_fkey" FOREIGN KEY ("deviceTrendInfoID") REFERENCES public.device_trend_infos(id);


--
-- Name: events events_sensorID_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bray_tamu
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT "events_sensorID_fkey" FOREIGN KEY ("sensorID") REFERENCES public.sensors(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: bray_tamu
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

