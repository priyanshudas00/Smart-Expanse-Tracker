from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_add_expense():
    response = client.post("/expenses", json={
        "title": "Lunch",
        "amount": 12.5,
        "category": "Food",
        "date": "2026-07-31"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Lunch"
    assert data["amount"] == 12.5
    assert data["category"] == "Food"
    assert data["date"] == "2026-07-31"

def test_view_all_expenses():
    # Add two expenses to have some data
    client.post("/expenses", json={"title": "Coffee", "amount": 3.0, "category": "Food", "date": "2026-07-31"})
    client.post("/expenses", json={"title": "Uber", "amount": 20.0, "category": "Transport", "date": "2026-07-31"})
    response = client.get("/expenses")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2

def test_filter_by_category():
    response = client.get("/expenses?category=Food")
    assert response.status_code == 200
    data = response.json()
    assert all(exp["category"] == "Food" for exp in data)

def test_total_overall():
    # Clear and add known amounts
    global expenses
    from src import main
    main.expenses.clear()
    main.next_id = 1
    client.post("/expenses", json={"title": "A", "amount": 10.0, "category": "A", "date": "2026-07-31"})
    client.post("/expenses", json={"title": "B", "amount": 20.0, "category": "B", "date": "2026-07-31"})
    response = client.get("/expenses/total")
    data = response.json()
    assert data["overall_total"] == 30.0
    assert "by_category" in data
    assert data["by_category"]["A"] == 10.0
    assert data["by_category"]["B"] == 20.0

def test_total_by_category():
    response = client.get("/expenses/total?category=A")
    data = response.json()
    assert data["category"] == "A"
    assert data["total"] == 10.0

def test_delete_existing_expense():
    # Add one to delete
    resp = client.post("/expenses", json={"title": "D", "amount": 1.0, "category": "D", "date": "2026-07-31"})
    eid = resp.json()["id"]
    response = client.delete(f"/expenses/{eid}")
    assert response.status_code == 200
    # Confirm it's gone
    get_resp = client.get("/expenses")
    ids = [e["id"] for e in get_resp.json()]
    assert eid not in ids

def test_delete_nonexistent_expense():
    response = client.delete("/expenses/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"