def test_create_organisation_returns_201(client):
	data = { "name": "test_org", "country": "test_cou", "type": "test_typ", "administrator": "test_adm", "website": "test_web" }

	response = client.post("/organisations", json=data)
	assert response.status_code == 201

	body = response.json()
	assert body["name"] == data["name"]


def test_get_organisation_by_id(client):
	data = { "name": "test_org", "country": "test_cou", "type": "test_typ", "administrator": "test_adm", "website": "test_web" }
	
	response = client.post("/organisations", json=data)
	assert response.status_code == 201

	get = client.get(f"/organisations/{response.json()["id"]}")
	assert get.status_code == 200
	assert get.json()["name"] == data["name"]


def test_update_organisation(client):
	data = { "name": "test_org", "country": "test_cou", "type": "test_typ", "administrator": "test_adm", "website": "test_web" }
		
	response = client.post("/organisations", json=data)
	assert response.status_code == 201

	get = client.get(f"/organisations/{response.json()["id"]}")
	assert get.status_code == 200

	put_data = { "name": "test_org_p", "country": "test_cou_p", "type": "test_typ_p", "administrator": "test_adm_p", "website": "test_web_p" }

	put = client.put(f"/organisations/{response.json()["id"]}", json=put_data)
	assert put.status_code == 200

	get = client.get(f"/organisations/{put.json()["id"]}")
	assert get.status_code == 200

	assert put.json()["name"] == put_data["name"]