from conftest import make_location, make_launchpad

def test_create_location_and_get_location(client):
	data = { "name": "test_loc", "country": "test_cou", "region": "test_reg" }

	response = client.post("/locations", json=data)
	assert response.status_code == 201

	response = client.get(f"/locations/{response.json()["id"]}")
	assert response.status_code == 200

	body = response.json()
	assert body["name"] == data["name"]
	assert body["country"] == data["country"]
	assert body["region"] == data["region"]

def test_get_unknown_id(client):
	response = client.get("/locations/99999")
	assert response.status_code == 404

def test_create_2_and_get_with_filter(client):
	data_1 = { "name": "test_loc_1", "country": "test_cou_1", "region": "test_reg_1" }
	data_2 = { "name": "test_loc_2", "country": "test_cou_2", "region": "test_reg_2" }

	response_1 = client.post("/locations", json=data_1)
	assert response_1.status_code == 201
	body_1 = response_1.json()

	response_2 = client.post("/locations", json=data_2)
	assert response_2.status_code == 201
	body_2 = response_2.json()

	response = client.get("/locations")
	assert response.status_code == 200
	body = response.json()

	assert str(body_1["id"]) in body
	assert str(body_2["id"]) in body

	response_filtered = client.get("/locations?country=test_cou_1")
	assert response_filtered.status_code == 200
	body_filtered = response_filtered.json()

	assert str(body_1["id"]) in body_filtered
	assert str(body_2["id"]) not in body_filtered

def test_update_location(client):
	loc = make_location(client)

	put_data = { "name": "test_loc_p", "country": "test_cou_p", "region": "test_reg_p" }

	put = client.put(f"/locations/{loc["id"]}", json=put_data)
	assert put.status_code == 200

	get = client.get(f"/locations/{put.json()["id"]}")
	assert get.status_code == 200

	assert get.json()["name"] == put_data["name"]

def test_update_on_unknown_id(client):
	put_data = { "name": "test_loc_p", "country": "test_cou_p", "region": "test_reg_p" }

	put = client.put(f"/locations/99999", json=put_data)
	assert put.status_code == 404

def test_delete_and_get_returns_404(client):
	loc = make_location(client)

	delete = client.delete(f"/locations/{loc["id"]}")
	assert delete.status_code == 204

	get = client.get(f"/locations/{loc["id"]}")
	assert get.status_code == 404

def test_create_with_incomplete_data(client):
	data = { "country": "test_cou", "region": "test_reg" } # Name missing

	response = client.post("/locations", json=data)
	assert response.status_code == 422

def test_delete_with_unknown_id(client):
	delete = client.delete(f"/locations/99999")
	assert delete.status_code == 404

def test_delete_with_reference_to_row(client):
	pad = make_launchpad(client)

	delete = client.delete(f"/locations/{pad["location_id"]}")
	assert delete.status_code == 409

	get = client.get(f"/locations/{pad["location_id"]}")
	assert get.status_code == 200
