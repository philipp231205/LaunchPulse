CREATE TABLE IF NOT EXISTS organisations (
	id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name text NOT NULL,
	country text,
	type text,
	administrator text,
	website text
);

CREATE TABLE IF NOT EXISTS locations (
	id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name text NOT NULL,
	country text,
	region text
);

CREATE TABLE IF NOT EXISTS launchpads (
	id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name text NOT NULL,
	longitude NUMERIC(9,6) NOT NULL,
	latitude NUMERIC(9,6) NOT NULL,
	status text,
	organisation_id bigint REFERENCES organisations(id),
	location_id bigint REFERENCES locations(id)
);

CREATE TABLE IF NOT EXISTS vehicles (
	id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name text NOT NULL,
	family text,
	height_m NUMERIC(6,2),
	diameter_m NUMERIC(5,2),
	mass_kg INTEGER,
	payload_leo_kg INTEGER,
	payload_gto_kg INTEGER,
	payload_sso_kg INTEGER,
	stages smallint,
	first_flight timestamptz,
	thrust_kn NUMERIC(8,1),
	status text,
	organisation_id bigint REFERENCES organisations(id)
);

CREATE TABLE IF NOT EXISTS launches (
	id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	date timestamptz NOT NULL,
	status text,
	webcast_url text,
	mission text NOT NULL,
	payload text,
	vehicle_id bigint REFERENCES vehicles(id) NOT NULL,
	launchpad_id bigint REFERENCES launchpads(id) NOT NULL,
	organisation_id bigint REFERENCES organisations(id)
);