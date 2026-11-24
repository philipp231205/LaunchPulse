import os
from dotenv import load_dotenv
load_dotenv()
os.environ["DATABASE_URL"] = os.environ["TEST_DATABASE_URL"]

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