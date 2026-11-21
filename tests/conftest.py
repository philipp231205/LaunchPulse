import os
from dotenv import load_dotenv
load_dotenv()
os.environ["DATABASE_URL"] = os.environ["TEST_DATABASE_URL"]

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)