import os
from dotenv import load_dotenv
load_dotenv()
os.environ["DATABASE_URL"] = os.environ["TEST_DATABASE_URL"]

from datetime import datetime

from fastapi.testclient import TestClient
from main import app
from app.db import get_conn

import pytest

@pytest.fixture
def client():
	return TestClient(app)

@pytest.fixture(autouse=True)
def clean_db():
	with get_conn() as conn:
		conn.execute("TRUNCATE organisations, locations, launchpads, vehicles, launches RESTART IDENTITY CASCADE")

def make_org(client):
	data = { "name": "test_org", "country": "test_cou", "type": "test_typ", "administrator": "test_adm", "website": "test_web" }

	response = client.post("/organisations", json=data)
	assert response.status_code == 201

	return response.json()

def make_location(client):
	data = { "name": "test_loc", "country": "test_cou", "region": "test_reg" }

	response = client.post("/locations", json=data)
	assert response.status_code == 201

	return response.json()

def make_launchpad(client):
	org = make_org(client)
	loc = make_location(client)

	data = {
		"name": "test_pad",
		"longitude": 0.0,
		"latitude": 0.0,
		"status": "test_sta",
		"organisation_id": org["id"],
		"location_id": loc["id"]
	}

	response = client.post("/launchpads", json=data)
	assert response.status_code == 201

	return response.json()

def make_vehicle(client):
	org = make_org(client)

	data = { 
		"name": "test_veh", 
		"family": "test_fam", 
		"height_m": 0.0,
		"diameter_m": 0.0,
		"mass_kg": 0,
		"payload_leo_kg": 0,
		"payload_gto_kg": 0,
		"payload_sso_kg": 0,
		"stages": 0,
		"first_flight": datetime.today().isoformat(),
		"thrust_kn": 0.0,
		"status": "test_sta",
		"organisation_id": org["id"]
	}

	response = client.post("/vehicles", json=data)
	assert response.status_code == 201

	return response.json()

def make_launch(client):
	veh = make_vehicle(client)
	pad = make_launchpad(client)

	data = {
		"date": "2026-01-15T12:00:00Z",
		"status": "test_sta",
		"webcast_url": "test_web",
		"mission": "test_mis",
		"payload": "test_pay",
		"vehicle_id": veh["id"],
		"launchpad_id": pad["id"],
		"organisation_id": veh["organisation_id"]
	}

	response = client.post("/launches", json=data)
	assert response.status_code == 201

	return response.json()