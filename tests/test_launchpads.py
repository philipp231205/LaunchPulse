from conftest import make_org, make_location, make_launchpad, make_launch

def test_create_launchpad_and_get_launchpad(client):
	org = make_org(client)
	loc = make_location(client)

	data = {
		"name": "test_pad",
		"longitude": "0.000000",
		"latitude": "0.000000",
		"status": "test_sta",
		"organisation_id": org["id"],
		"location_id": loc["id"]
	}

	response = client.post("/launchpads", json=data)
	assert response.status_code == 201

	response = client.get(f"/launchpads/{response.json()["id"]}")
	assert response.status_code == 200

	body = response.json()
	assert body["name"] == data["name"]
	assert body["longitude"] == data["longitude"]
	assert body["latitude"] == data["latitude"]
	assert body["status"] == data["status"]
	assert body["organisation_id"] == data["organisation_id"]
	assert body["location_id"] == data["location_id"]

def test_get_unknown_id(client):
	response = client.get("/launchpads/99999")
	assert response.status_code == 404

def test_create_2_and_get_with_filter(client):
	org = make_org(client)
	loc = make_location(client)

	data_1 = {
		"name": "test_pad_1",
		"longitude": 1.0,
		"latitude": 2.0,
		"status": "test_sta_1",
		"organisation_id": org["id"],
		"location_id": loc["id"]
	}
	data_2 = {
		"name": "test_pad_2",
		"longitude": 3.0,
		"latitude": 4.0,
		"status": "test_sta_2",
		"organisation_id": org["id"],
		"location_id": loc["id"]
	}

	response_1 = client.post("/launchpads", json=data_1)
	assert response_1.status_code == 201
	body_1 = response_1.json()

	response_2 = client.post("/launchpads", json=data_2)
	assert response_2.status_code == 201
	body_2 = response_2.json()

	response = client.get("/launchpads")
	assert response.status_code == 200
	body = response.json()

	assert str(body_1["id"]) in body
	assert str(body_2["id"]) in body

	response_filtered = client.get("/launchpads?status=test_sta_1")
	assert response_filtered.status_code == 200
	body_filtered = response_filtered.json()

	assert str(body_1["id"]) in body_filtered
	assert str(body_2["id"]) not in body_filtered

def test_update_launchpad(client):
	pad = make_launchpad(client)

	put_data = {
		"name": "test_pad_p",
		"longitude": 11.0,
		"latitude": 22.0,
		"status": "test_sta_p",
		"organisation_id": pad["organisation_id"],
		"location_id": pad["location_id"]
	}

	put = client.put(f"/launchpads/{pad["id"]}", json=put_data)
	assert put.status_code == 200

	get = client.get(f"/launchpads/{put.json()["id"]}")
	assert get.status_code == 200

	assert get.json()["name"] == put_data["name"]

def test_update_on_unknown_id(client):
	put_data = {
		"name": "test_pad_p",
		"longitude": 11.0,
		"latitude": 22.0,
		"status": "test_sta_p",
		"organisation_id": 1,
		"location_id": 1
	}

	put = client.put(f"/launchpads/99999", json=put_data)
	assert put.status_code == 404

def test_delete_and_get_returns_404(client):
	pad = make_launchpad(client)

	delete = client.delete(f"/launchpads/{pad["id"]}")
	assert delete.status_code == 204

	get = client.get(f"/launchpads/{pad["id"]}")
	assert get.status_code == 404

def test_create_with_incomplete_data(client):
	data = { "longitude": 0.0, "latitude": 0.0, "status": "test_sta", "organisation_id": 1, "location_id": 1 } # Name missing

	response = client.post("/launchpads", json=data)
	assert response.status_code == 422

def test_delete_with_unknown_id(client):
	delete = client.delete(f"/launchpads/99999")
	assert delete.status_code == 404

def test_delete_with_reference_to_row(client):
	launch = make_launch(client)

	delete = client.delete(f"/launchpads/{launch["launchpad_id"]}")
	assert delete.status_code == 409

	get = client.get(f"/launchpads/{launch["launchpad_id"]}")
	assert get.status_code == 200
