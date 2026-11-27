from app import app, calculate_total


def client():
    return app.test_client()


def test_health():
    response = client().get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_menu_has_items():
    response = client().get("/menu")
    assert response.status_code == 200
    assert len(response.get_json()) == 3


def test_calculate_total():
    # 2 x Nasi Lemak (8.50) + 1 x Iced Milo (4.00) = 21.00
    items = [{"id": 2, "qty": 2}, {"id": 3, "qty": 1}]
    assert calculate_total(items) == 21.00


def test_create_order():
    response = client().post("/orders", json={"items": [{"id": 1, "qty": 1}]})
    assert response.status_code == 201
    assert response.get_json()["total"] == 12.90


def test_empty_order_rejected():
    response = client().post("/orders", json={"items": []})
    assert response.status_code == 400


def test_feedback():
    response = client().post("/feedback", json={"message": "Delivery was fast!"})
    assert response.status_code == 201