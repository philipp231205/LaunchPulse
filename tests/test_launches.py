from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_create_then_list_launch():
	new_launch = {
		"rocket": "CI Test Rocket",
		"provider": "GitHub Actions",
		"launch_time": "2030-01-01T12:00:00Z",
		"status": "upcoming",
		"is_crewed": True,
		"webcast_url": "github.com"
	}
	created = client.post("/launches/create", json=new_launch)
	assert created.status_code == 200
	launch_id = created.json()["id"]

	listed = client.get("/launches")
	assert listed.status_code == 200
	ids = [launch["id"] for launch in listed.json().values()]
	assert launch_id in ids
