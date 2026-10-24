from tests.conftest import auth_headers

PRODUCT = {"name": "Laptop", "description": "14 inch", "price": "999.99", "stock": 5}


def test_register_and_login(client):
    res = client.post(
        "/auth/register", json={"email": "a@example.com", "password": "password123"}
    )
    assert res.status_code == 201
    res = client.post(
        "/auth/login", data={"username": "a@example.com", "password": "password123"}
    )
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_duplicate_email_rejected(client):
    body = {"email": "a@example.com", "password": "password123"}
    client.post("/auth/register", json=body)
    assert client.post("/auth/register", json=body).status_code == 409


def test_wrong_password_rejected(client):
    client.post(
        "/auth/register", json={"email": "a@example.com", "password": "password123"}
    )
    res = client.post(
        "/auth/login", data={"username": "a@example.com", "password": "wrongpass1"}
    )
    assert res.status_code == 401


def test_customer_cannot_create_product(client, user_headers):
    res = client.post("/products", json=PRODUCT, headers=user_headers)
    assert res.status_code == 403


def test_admin_creates_and_lists_product(client, admin_headers):
    res = client.post("/products", json=PRODUCT, headers=admin_headers)
    assert res.status_code == 201
    listing = client.get("/products", params={"q": "lap"})
    assert len(listing.json()) == 1


def test_place_order_reduces_stock(client, admin_headers, user_headers):
    product = client.post("/products", json=PRODUCT, headers=admin_headers).json()
    res = client.post(
        "/orders",
        json={"items": [{"product_id": product["id"], "quantity": 2}]},
        headers=user_headers,
    )
    assert res.status_code == 201
    assert float(res.json()["total"]) == 1999.98
    assert client.get(f"/products/{product['id']}").json()["stock"] == 3


def test_order_fails_when_out_of_stock(client, admin_headers, user_headers):
    product = client.post("/products", json=PRODUCT, headers=admin_headers).json()
    res = client.post(
        "/orders",
        json={"items": [{"product_id": product["id"], "quantity": 10}]},
        headers=user_headers,
    )
    assert res.status_code == 400


def test_user_cannot_see_other_users_order(client, admin_headers, user_headers):
    product = client.post("/products", json=PRODUCT, headers=admin_headers).json()
    order = client.post(
        "/orders",
        json={"items": [{"product_id": product["id"], "quantity": 1}]},
        headers=user_headers,
    ).json()

    other = auth_headers(client, "other@example.com")
    assert client.get(f"/orders/{order['id']}", headers=other).status_code == 404


def test_admin_updates_order_status(client, admin_headers, user_headers):
    product = client.post("/products", json=PRODUCT, headers=admin_headers).json()
    order = client.post(
        "/orders",
        json={"items": [{"product_id": product["id"], "quantity": 1}]},
        headers=user_headers,
    ).json()
    res = client.patch(
        f"/orders/{order['id']}/status",
        json={"status": "shipped"},
        headers=admin_headers,
    )
    assert res.status_code == 200
    assert res.json()["status"] == "shipped"