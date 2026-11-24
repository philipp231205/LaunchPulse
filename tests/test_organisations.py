from conftest import make_org, make_vehicle

def test_create_organisation_and_get_organisation(client):
	data = { "name": "test_org", "country": "test_cou", "type": "test_typ", "administrator": "test_adm", "website": "test_web" }

	response = client.post("/organisations", json=data)
	assert response.status_code == 201

	response = client.get(f"/organisations/{response.json()["id"]}")
	assert response.status_code == 200

	body = response.json()
	assert body["name"] == data["name"]
	assert body["country"] == data["country"]
	assert body["type"] == data["type"]
	assert body["administrator"] == data["administrator"]
	assert body["website"] == data["website"]

def test_get_unknown_id(client):
	response = client.get("/organisations/99999")
	assert response.status_code == 404

def test_create_2_and_get_with_filter(client):
	data_1 = { "name": "test_org_1", "country": "test_cou_1", "type": "test_typ_1", "administrator": "test_adm_1", "website": "test_web_1" }
	data_2 = { "name": "test_org_2", "country": "test_cou_2", "type": "test_typ_2", "administrator": "test_adm_2", "website": "test_web_2" }

	response_1 = client.post("/organisations", json=data_1)
	assert response_1.status_code == 201
	body_1 = response_1.json()

	response_2 = client.post("/organisations", json=data_2)
	assert response_2.status_code == 201
	body_2 = response_2.json()

	response = client.get("/organisations")
	assert response.status_code == 200
	body = response.json()

	assert body[str(body_1["id"])]["name"] == data_1["name"]
	assert body[str(body_2["id"])]["name"] == data_2["name"]

	response_filtered = client.get("/organisations?type=test_typ_1")
	assert response_filtered.status_code == 200
	body_filtered = response_filtered.json()

	assert body_filtered[str(body_1["id"])]["name"] == data_1["name"]

def test_update_organisation(client):
	response = make_org(client)

	put_data = { "name": "test_org_p", "country": "test_cou_p", "type": "test_typ_p", "administrator": "test_adm_p", "website": "test_web_p" }

	put = client.put(f"/organisations/{response["id"]}", json=put_data)
	assert put.status_code == 200

	get = client.get(f"/organisations/{put.json()["id"]}")
	assert get.status_code == 200

	assert get.json()["name"] == put_data["name"]

def test_update_on_unknown_id(client):
	put_data = { "name": "test_org_p", "country": "test_cou_p", "type": "test_typ_p", "administrator": "test_adm_p", "website": "test_web_p" }

	put = client.put(f"/organisations/99999", json=put_data)
	assert put.status_code == 404

def test_delete_and_get_returns_404(client):
	response = make_org(client)

	delete = client.delete(f"/organisations/{response["id"]}")
	assert delete.status_code == 204

	get = client.get(f"/organisations/{response["id"]}")
	assert get.status_code == 404

def test_create_with_incomplete_data(client):
	data = { "country": "test_cou", "type": "test_typ", "administrator": "test_adm", "website": "test_web" } # Name missing

	response = client.post("/organisations", json=data)
	assert response.status_code == 422

def test_delete_with_reference_to_row(client):
	veh = make_vehicle(client)

	delete = client.delete(f"/organisations/{veh["organisation_id"]}")
	assert delete.status_code == 409