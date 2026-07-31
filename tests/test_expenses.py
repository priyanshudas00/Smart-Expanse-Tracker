import importlib
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(tmp_path, monkeypatch):
    data_file = tmp_path / "expenses.json"
    monkeypatch.setenv("EXPENSES_FILE", str(data_file))

    import src.main as main

    importlib.reload(main)
    return TestClient(main.app)


def test_create_and_list_expenses(client):
    payload = {
        "title": "Lunch",
        "amount": 12.5,
        "category": "Food",
        "date": "2026-07-31",
    }

    create_response = client.post("/expenses", json=payload)
    assert create_response.status_code == 201
    assert create_response.json()["id"] == 1

    list_response = client.get("/expenses")
    assert list_response.status_code == 200
    data = list_response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Lunch"


def test_filter_by_category_and_summary(client):
    client.post(
        "/expenses",
        json={
            "title": "Lunch",
            "amount": 15.0,
            "category": "Food",
            "date": "2026-07-31",
        },
    )
    client.post(
        "/expenses",
        json={
            "title": "Taxi",
            "amount": 20.0,
            "category": "Travel",
            "date": "2026-07-31",
        },
    )

    filtered_response = client.get("/expenses", params={"category": "Food"})
    assert filtered_response.status_code == 200
    assert [item["id"] for item in filtered_response.json()] == [1]

    summary_response = client.get("/expenses/summary")
    assert summary_response.status_code == 200
    body = summary_response.json()
    assert body["total"] == 35.0
    assert body["by_category"]["Food"] == 15.0
    assert body["by_category"]["Travel"] == 20.0


def test_delete_expense(client):
    client.post(
        "/expenses",
        json={
            "title": "Coffee",
            "amount": 4.5,
            "category": "Food",
            "date": "2026-07-31",
        },
    )

    delete_response = client.delete("/expenses/1")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Expense deleted successfully"

    list_response = client.get("/expenses")
    assert list_response.json() == []


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Smart Expense Tracker API is running"
