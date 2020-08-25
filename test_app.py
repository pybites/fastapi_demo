import pytest

from fastapi.testclient import TestClient

from app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_get_all_bites(client):
    response = client.get("/")
    assert response.status_code == 200
    expected = {
        '1': {"name": "Sum of numbers", "level": 2},
        '2': {"name": "Regex fun", "description": "regex are ...", "level": 4},
        '3': {"name": "Word values", "level": 3},
    }
    assert response.json() == expected


@pytest.mark.parametrize("idx, expected", [
    (1, {"name": "Sum of numbers", "level": 2}),
    (2, {"name": "Regex fun", "description": "regex are ...", "level": 4}),
    (3, {"name": "Word values", "level": 3}),
])
def test_get_first_bite(client, idx, expected):
    response = client.get(f"/{idx}")
    assert response.status_code == 200
    assert response.json() == expected


def test_bite_not_found(client):
    response = client.get("/4")
    assert response.status_code == 404
    assert "Bite not found" in str(response._content)


def test_add_bite(client):
    response = client.get("/").json()
    num_objects_before = len(response)
    new_bite = {"name": "Top 10 PyBites tags", "level": "3"}
    response = client.post("/", json=new_bite)
    assert response.status_code == 201
    expected = {'description': None, 'level': 3,
                'name': 'Top 10 PyBites tags', 'tags': []}
    assert response.json() == expected
    response = client.get("/").json()
    num_objects_after = len(response)
    assert num_objects_after - num_objects_before == 1
    assert response.get(str(num_objects_after)) == expected


def test_update_bite(client):
    response = client.get("/3").json()
    assert response == {'name': 'Word values', 'level': 3}
    updated_bite = {'name': 'Word values II', 'level': 4}
    response = client.put("/3", json=updated_bite)
    response = client.get("/3").json()
    assert response == {'name': 'Word values II',
                        'description': None, 'level': 4, 'tags': []}


def test_delete_bite(client):
    response = client.get("/").json()
    count_before = len(response)
    response = client.delete("/3")
    assert response.status_code == 204
    assert response.json() == {}
    response = client.get("/").json()
    count_after = len(response)
    assert count_before - count_after == 1
    response = client.get("/3")
    assert response.status_code == 404
