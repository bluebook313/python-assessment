import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path
APP_DIR = Path(__file__).resolve().parent.parent / "app"
sys.path.insert(0, str(APP_DIR))
from app.main import app
server_ip = "http://127.0.0.1"
port = 8000
version= "v1"
@pytest.fixture
def client():
    return TestClient(app)

def test_complete_order_flow(client):

    # 1. Create customer
    response = client.post(
        f"/{version}/customer/add_customer/",
        params={
            "name": "Ali",
            "email": "ali@test.com",
        },
    )
    assert response.status_code == 200
    
    customer_id = response.json()["Result"]["Id"]

    # 2. Add product
    response = client.post(
        f"{version}/products/add_product/",
        json={
            "name": "Laptop",
            "price": 1000,
            "product_count": 10,
        },
    )

    assert response.status_code == 200

    product_id = response.json()["Result"]["Id"]

    # 3. Create empty order
    response = client.post(
        f"{version}/orders/add_new_empty_order",
        params={
            "customer_id": customer_id,
        },
    )

    assert response.status_code == 200

    order_id = response.json()["Result"]["Id"]

    # 4. Add product to basket
    response = client.post(
        f"{version}/orders/add_product_to_basket",
        json={
            "order_id": order_id,
            "product_id": product_id,
            "product_count": 2,
        },
    )

    assert response.status_code == 200

    # 5. Pay order
    response = client.post(
        f"{version}/orders/{order_id}/pay",
    )

    assert response.status_code == 200

    # 6. Payment callback
    response = client.post(
        f"{version}/orders/{order_id}/pay_web_hook_answer",
        params={
            "payment_status": True,
        },
    )

    assert response.status_code == 200
    print(response.text)
    # 7. Verify final order
    response = client.get(
        f"{version}/orders/{order_id}",
    )

    assert response.status_code == 200
    print(response.text)
    order = response.json()["Result"]

    assert order["OrderId"] == order_id