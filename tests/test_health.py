import conftest

def test_health_returns_up():
	response = conftest.client.get("/health")
	assert response.status_code == 200