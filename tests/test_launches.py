from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_create_then_list_launch():
	new_launch = {
		"rocket": "CI Test Rocket",
		"provider": "GitHub Actions",
		"launch_time": "Today",
	}
	created = client.post("/launches", json=new_launch)
	assert created.status_code == 201
	launch_id = created.json()["id"]

	listed = client.get("/launches")
	assert listed.status_code == 200
	ids = [launch["id"] for launch in listed.json()]
	assert launch_id in ids
	