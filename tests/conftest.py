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