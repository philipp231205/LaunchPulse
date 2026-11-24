from conftest import make_org, make_vehicle, make_launch

def test_create_vehicle_and_get_vehicle(client):
	org = make_org(client)

	data = {
		"name": "test_veh",
		"family": "test_fam",
		"height_m": "0.00",
		"diameter_m": "0.00",
		"mass_kg": 0,
		"payload_leo_kg": 0,
		"payload_gto_kg": 0,
		"payload_sso_kg": 0,
		"stages": 0,
		"first_flight": "2026-01-15T12:00:00Z",
		"thrust_kn": "0.0",
		"status": "test_sta",
		"organisation_id": org["id"]
	}

	response = client.post("/vehicles", json=data)
	assert response.status_code == 201

	response = client.get(f"/vehicles/{response.json()["id"]}")
	assert response.status_code == 200

	body = response.json()
	assert body["name"] == data["name"]
	assert body["family"] == data["family"]
	assert body["height_m"] == data["height_m"]
	assert body["diameter_m"] == data["diameter_m"]
	assert body["mass_kg"] == data["mass_kg"]
	assert body["payload_leo_kg"] == data["payload_leo_kg"]
	assert body["payload_gto_kg"] == data["payload_gto_kg"]
	assert body["payload_sso_kg"] == data["payload_sso_kg"]
	assert body["stages"] == data["stages"]
	assert body["first_flight"] == data["first_flight"]
	assert body["thrust_kn"] == data["thrust_kn"]
	assert body["status"] == data["status"]
	assert body["organisation_id"] == data["organisation_id"]

def test_get_unknown_id(client):
	response = client.get("/vehicles/99999")
	assert response.status_code == 404

def test_create_2_and_get_with_filter(client):
	org = make_org(client)

	data_1 = {
		"name": "test_veh_1",
		"family": "test_fam_1",
		"height_m": 0.0,
		"diameter_m": 0.0,
		"mass_kg": 0,
		"payload_leo_kg": 0,
		"payload_gto_kg": 0,
		"payload_sso_kg": 0,
		"stages": 0,
		"first_flight": "2026-01-15T12:00:00+00:00",
		"thrust_kn": 0.0,
		"status": "test_sta_1",
		"organisation_id": org["id"]
	}
	data_2 = {
		"name": "test_veh_2",
		"family": "test_fam_2",
		"height_m": 1.0,
		"diameter_m": 1.0,
		"mass_kg": 1,
		"payload_leo_kg": 1,
		"payload_gto_kg": 1,
		"payload_sso_kg": 1,
		"stages": 1,
		"first_flight": "2026-02-15T12:00:00+00:00",
		"thrust_kn": 1.0,
		"status": "test_sta_2",
		"organisation_id": org["id"]
	}

	response_1 = client.post("/vehicles", json=data_1)
	assert response_1.status_code == 201
	body_1 = response_1.json()

	response_2 = client.post("/vehicles", json=data_2)
	assert response_2.status_code == 201
	body_2 = response_2.json()

	response = client.get("/vehicles")
	assert response.status_code == 200
	body = response.json()

	assert str(body_1["id"]) in body
	assert str(body_2["id"]) in body

	response_filtered = client.get("/vehicles?family=test_fam_1")
	assert response_filtered.status_code == 200
	body_filtered = response_filtered.json()

	assert str(body_1["id"]) in body_filtered
	assert str(body_2["id"]) not in body_filtered

def test_update_vehicle(client):
	veh = make_vehicle(client)

	put_data = {
		"name": "test_veh_p",
		"family": "test_fam_p",
		"height_m": 2.0,
		"diameter_m": 2.0,
		"mass_kg": 2,
		"payload_leo_kg": 2,
		"payload_gto_kg": 2,
		"payload_sso_kg": 2,
		"stages": 2,
		"first_flight": "2026-03-15T12:00:00+00:00",
		"thrust_kn": 2.0,
		"status": "test_sta_p",
		"organisation_id": veh["organisation_id"]
	}

	put = client.put(f"/vehicles/{veh["id"]}", json=put_data)
	assert put.status_code == 200

	get = client.get(f"/vehicles/{put.json()["id"]}")
	assert get.status_code == 200

	assert get.json()["name"] == put_data["name"]

def test_update_on_unknown_id(client):
	put_data = {
		"name": "test_veh_p",
		"family": "test_fam_p",
		"status": "test_sta_p",
		"organisation_id": 1
	}

	put = client.put(f"/vehicles/99999", json=put_data)
	assert put.status_code == 404

def test_delete_and_get_returns_404(client):
	veh = make_vehicle(client)

	delete = client.delete(f"/vehicles/{veh["id"]}")
	assert delete.status_code == 204

	get = client.get(f"/vehicles/{veh["id"]}")
	assert get.status_code == 404

def test_create_with_incomplete_data(client):
	data = { "family": "test_fam", "status": "test_sta", "organisation_id": 1 } # Name missing

	response = client.post("/vehicles", json=data)
	assert response.status_code == 422

def test_delete_with_unknown_id(client):
	delete = client.delete(f"/vehicles/99999")
	assert delete.status_code == 404

def test_delete_with_reference_to_row(client):
	launch = make_launch(client)

	delete = client.delete(f"/vehicles/{launch["vehicle_id"]}")
	assert delete.status_code == 409

	get = client.get(f"/vehicles/{launch["vehicle_id"]}")
	assert get.status_code == 200
