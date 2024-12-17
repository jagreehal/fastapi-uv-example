import pytest
from fastapi.testclient import TestClient

from .main import Todo, app, todos


@pytest.fixture(scope="function")
def client():
    todos.clear()  # Clear todos before each test
    with TestClient(app) as client:
        yield client


def setup_function():
    todos.clear()


buy_groceries_json = Todo(name="Buy groceries").model_dump()


def test_get_todos_when_no_todos_exist_should_return_empty_list(client):
    response = client.get("/todo")
    assert response.status_code == 200
    assert response.json() == []


def test_create_todo_when_valid_data_is_posted_should_create_todo(client):
    response = client.post("/todo", json=buy_groceries_json)
    assert response.status_code == 200
    assert response.json() == {"name": "Buy groceries", "completed": False}


def test_get_todo_when_todo_exists_should_return_todo(client):
    client.post("/todo", json=buy_groceries_json)
    response = client.get("/todo/1")
    assert response.status_code == 200
    assert response.json() == {"name": "Buy groceries", "completed": False}


def test_update_todo_when_todo_exists_should_update_todo(client):
    client.post("/todo", json=buy_groceries_json)
    response = client.put("/todo/1", json={"name": "Buy vegetables", "completed": True})
    assert response.status_code == 200
    assert response.json() == {"name": "Buy vegetables", "completed": True}


def test_delete_todo_when_todo_exists_should_delete_todo(client):
    client.post("/todo/", json=buy_groceries_json)
    response = client.delete("/todo/1")
    assert response.status_code == 200
    assert response.json() == {"name": "Buy groceries", "completed": False}


def test_get_todo_when_todo_does_not_exist_should_return_404_not_found(client):
    response = client.get("/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_update_todo_when_todo_does_not_exist_should_return_404_not_found(client):
    response = client.put(
        "/todo/999", json={"name": "Buy something", "completed": True}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo_when_todo_does_not_exist_should_return_404_not_found(client):
    response = client.delete("/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
