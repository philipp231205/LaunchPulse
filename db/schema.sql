CREATE TABLE IF NOT EXISTS organisations (
	id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name text NOT NULL,
	country text NOT NULL,
	type text NOT NULL,
	administrator text NOT NULL,
	website text NOT NULL
);

CREATE TABLE IF NOT EXISTS locations (
	id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name text NOT NULL,
	country text NOT NULL,
	region text NOT NULL
);

CREATE TABLE IF NOT EXISTS launchpads (
	id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name text NOT NULL,
	longitude NUMERIC(9,6) NOT NULL,
	latitude NUMERIC(9,6) NOT NULL,
	status text NOT NULL,
	organisation_id bigint REFERENCES organisations(id),
	location_id bigint REFERENCES locations(id)
);

CREATE TABLE IF NOT EXISTS vehicles (
	id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name text NOT NULL,
	family text NOT NULL,
	height_m NUMERIC(6,2) NOT NULL,
	diameter_m NUMERIC(5,2) NOT NULL,
	mass_kg INTEGER NOT NULL,
	payload_leo_kg INTEGER,
	payload_gto_kg INTEGER,
	payload_sso_kg INTEGER,
	stages smallint NOT NULL,
	first_flight TIMESTAMP NOT NULL,
	thrust_kn NUMERIC(8,1) NOT NULL,
	status text NOT NULL,
	organisation_id bigint REFERENCES organisations(id)
);

CREATE TABLE IF NOT EXISTS launches (
	id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	date TIMESTAMP NOT NULL,
	status text NOT NULL,
	webcast_url text,
	mission text NOT NULL,
	payload text NOT NULL,
	vehicle_id bigint REFERENCES vehicles(id),
	launchpad_id bigint REFERENCES launchpads(id),
	organisation_id bigint REFERENCES organisations(id)
);