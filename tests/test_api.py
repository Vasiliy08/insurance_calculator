from fastapi.testclient import TestClient
from httpx import Response


def test_upload_rates(client: TestClient):
    with open("rates.json", "rb") as json_file:
        response: Response = client.post("/upload-rates/", files={"file": ("data.json", json_file, "application/json")})
    assert response.status_code == 201
    assert response.json() == {"message": "Данные успешно обновлены"}


def test_upload_rates_invalid_json(client: TestClient):
    with open("invalid_rates.json", "rb") as json_file:
        response: Response = client.post("/upload-rates/", files={"file": ("data.json", json_file, "application/json")})
    assert response.status_code == 400


def test_calculate_insurance(client: TestClient):
    response = client.get("/calculate/", params={"cargo_type": "Glass", "declared_value": 1000.0, "date": "2024-01-01"})
    assert response.status_code == 200
    assert "Стоимость" in response.json()


def test_calculate_insurance_not_found(client: TestClient):
    response = client.get(
        "/calculate/", params={"cargo_type": "nonexistent", "declared_value": 1000.0, "date": "2024-01-01"}
    )
    assert response.status_code == 400


def test_get_all_rates(client: TestClient):
    response = client.get("/rates/", params={"offset": 0, "limit": 5, "order_by": "asc"})
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"]["items"], list)


def test_get_all_rates_empty(client: TestClient):
    response = client.get("/rates/", params={"offset": 0, "limit": 0, "order_by": "asc"})
    assert response.status_code == 200
    assert response.json()["data"]["items"] == []


def test_get_all_rates_with_pagination(client: TestClient):
    response = client.get("/rates/", params={"offset": 0, "limit": 1, "order_by": "asc"})
    assert response.status_code == 200
    assert "data" in response.json()
    assert len(response.json()["data"]["items"]) <= 1
