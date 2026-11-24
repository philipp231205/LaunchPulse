from conftest import make_vehicle, make_launchpad, make_launch

def test_create_launch_and_get_launch(client):
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

	response = client.get(f"/launches/{response.json()["id"]}")
	assert response.status_code == 200

	body = response.json()
	assert body["date"] == data["date"]
	assert body["status"] == data["status"]
	assert body["webcast_url"] == data["webcast_url"]
	assert body["mission"] == data["mission"]
	assert body["payload"] == data["payload"]
	assert body["vehicle_id"] == data["vehicle_id"]
	assert body["launchpad_id"] == data["launchpad_id"]
	assert body["organisation_id"] == data["organisation_id"]

def test_get_unknown_id(client):
	response = client.get("/launches/99999")
	assert response.status_code == 404

def test_create_2_and_get_with_filter(client):
	veh = make_vehicle(client)
	pad = make_launchpad(client)

	data_1 = {
		"date": "2026-01-15T12:00:00+00:00",
		"status": "test_sta_1",
		"webcast_url": "test_web_1",
		"mission": "test_mis_1",
		"payload": "test_pay_1",
		"vehicle_id": veh["id"],
		"launchpad_id": pad["id"],
		"organisation_id": veh["organisation_id"]
	}
	data_2 = {
		"date": "2026-02-15T12:00:00+00:00",
		"status": "test_sta_2",
		"webcast_url": "test_web_2",
		"mission": "test_mis_2",
		"payload": "test_pay_2",
		"vehicle_id": veh["id"],
		"launchpad_id": pad["id"],
		"organisation_id": veh["organisation_id"]
	}

	response_1 = client.post("/launches", json=data_1)
	assert response_1.status_code == 201
	body_1 = response_1.json()

	response_2 = client.post("/launches", json=data_2)
	assert response_2.status_code == 201
	body_2 = response_2.json()

	response = client.get("/launches")
	assert response.status_code == 200
	body = response.json()

	assert str(body_1["id"]) in body
	assert str(body_2["id"]) in body

	response_filtered = client.get("/launches?status=test_sta_1")
	assert response_filtered.status_code == 200
	body_filtered = response_filtered.json()

	assert str(body_1["id"]) in body_filtered
	assert str(body_2["id"]) not in body_filtered

def test_update_launch(client):
	launch = make_launch(client)

	put_data = {
		"date": "2026-03-15T12:00:00+00:00",
		"status": "test_sta_p",
		"webcast_url": "test_web_p",
		"mission": "test_mis_p",
		"payload": "test_pay_p",
		"vehicle_id": launch["vehicle_id"],
		"launchpad_id": launch["launchpad_id"],
		"organisation_id": launch["organisation_id"]
	}

	put = client.put(f"/launches/{launch["id"]}", json=put_data)
	assert put.status_code == 200

	get = client.get(f"/launches/{put.json()["id"]}")
	assert get.status_code == 200

	assert get.json()["mission"] == put_data["mission"]

def test_update_on_unknown_id(client):
	put_data = {
		"date": "2026-03-15T12:00:00+00:00",
		"status": "test_sta_p",
		"webcast_url": "test_web_p",
		"mission": "test_mis_p",
		"payload": "test_pay_p",
		"vehicle_id": 1,
		"launchpad_id": 1,
		"organisation_id": 1
	}

	put = client.put(f"/launches/99999", json=put_data)
	assert put.status_code == 404

def test_delete_and_get_returns_404(client):
	launch = make_launch(client)

	delete = client.delete(f"/launches/{launch["id"]}")
	assert delete.status_code == 204

	get = client.get(f"/launches/{launch["id"]}")
	assert get.status_code == 404

def test_create_with_incomplete_data(client):
	data = {
		"date": "2026-01-15T12:00:00+00:00",
		"status": "test_sta",
		"webcast_url": "test_web",
		"payload": "test_pay",
		"vehicle_id": 1,
		"launchpad_id": 1,
		"organisation_id": 1
	} # Mission missing

	response = client.post("/launches", json=data)
	assert response.status_code == 422

def test_delete_with_unknown_id(client):
	delete = client.delete(f"/launches/99999")
	assert delete.status_code == 404
