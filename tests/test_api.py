import pytest


@pytest.mark.parametrize(
    "payload",
    [
        {
            "title": "Омлет",
            "cooking_time": 10,
            "ingredients": "яйца, молоко, соль",
            "description": "Быстрый завтрак",
        },
        {
            "title": "Паста",
            "cooking_time": 25,
            "ingredients": "паста, соус, сыр",
            "description": "Простой ужин",
        },
    ],
)
def test_create_recipe(client, payload):
    response = client.post("/recipes", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == payload["title"]


def test_get_recipes(client):
    response = client.get("/recipes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_recipe_and_increment_views(client):
    create_response = client.post(
        "/recipes",
        json={
            "title": "Суп",
            "cooking_time": 40,
            "ingredients": "вода, картофель, морковь",
            "description": "Домашний суп",
        },
    )
    recipe_id = create_response.json()["id"]

    first = client.get(f"/recipes/{recipe_id}")
    assert first.status_code == 200
    first_data = first.json()
    assert first_data["id"] == recipe_id
    assert first_data["views"] == 1

    second = client.get(f"/recipes/{recipe_id}")
    assert second.status_code == 200
    second_data = second.json()
    assert second_data["views"] == 2
