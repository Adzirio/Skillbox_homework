import pytest


@pytest.mark.parametrize(
    "method,url",
    [
        ("get", "/clients"),
    ],
)
def test_get_routes_return_200(client, method, url):
    response = getattr(client, method)(url)
    assert response.status_code == 200


def test_get_client_create_and_fetch(client):
    create_response = client.post(
        "/clients",
        json={
            "name": "Test",
            "surname": "User",
            "credit_card": "1234",
            "car_number": "TEST123",
        },
    )
    assert create_response.status_code == 201
    client_id = create_response.get_json()["id"]

    response = client.get(f"/clients/{client_id}")
    assert response.status_code == 200


def test_create_client(client):
    response = client.post(
        "/clients",
        json={
            "name": "Petr",
            "surname": "Ivanov",
            "credit_card": "5555444433332222",
            "car_number": "B456CD",
        },
    )
    assert response.status_code == 201
    assert "id" in response.get_json()


def test_create_parking(client):
    response = client.post(
        "/parkings",
        json={
            "address": "Lenina 10",
            "opened": True,
            "count_places": 20,
            "count_available_places": 20,
        },
    )
    assert response.status_code == 201
    assert "id" in response.get_json()


@pytest.mark.parking
def test_enter_parking(client):
    client_resp = client.post(
        "/clients", json={"name": "Test", "surname": "Testov", "credit_card": "1234"}
    )
    parking_resp = client.post(
        "/parkings",
        json={
            "address": "Test",
            "opened": True,
            "count_places": 5,
            "count_available_places": 5,
        },
    )

    client_id = client_resp.get_json()["id"]
    parking_id = parking_resp.get_json()["id"]

    response = client.post(
        "/client_parkings", json={"client_id": client_id, "parking_id": parking_id}
    )
    assert response.status_code == 201


@pytest.mark.parking
def test_leave_parking(client):
    client_resp = client.post(
        "/clients", json={"name": "Test", "surname": "Testov", "credit_card": "1234"}
    )
    parking_resp = client.post(
        "/parkings",
        json={
            "address": "Test",
            "opened": True,
            "count_places": 5,
            "count_available_places": 5,
        },
    )

    client_id = client_resp.get_json()["id"]
    parking_id = parking_resp.get_json()["id"]

    client.post(
        "/client_parkings", json={"client_id": client_id, "parking_id": parking_id}
    )
    response = client.delete(
        "/client_parkings", json={"client_id": client_id, "parking_id": parking_id}
    )
    assert response.status_code == 200


######################


def test_create_client_factory(client):
    """Дубликат test_create_client с Factory Boy"""
    from tests.factories import client_factory

    client_data = client_factory()

    response = client.post("/clients", json=client_data)

    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data  # Проверяем что возвращает API


def test_create_parking_factory(client):
    """Дубликат test_create_parking с Factory Boy"""
    from tests.factories import parking_factory

    parking_data = parking_factory()

    response = client.post("/parkings", json=parking_data)

    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data  # Проверяем что возвращает API
