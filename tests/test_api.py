import requests

def test_health():
    response = requests.get("http://127.0.0.1:9000/health")

    assert response.status_code == 200
    assert response.text.strip() == "healthy"

def test_create_item():
    response = requests.post(
      "http://127.0.0.1:9000/items",
      json={"name": "ci-monitor"}
    )
    assert response.status_code == 201

    itemcheck = requests.get("http://127.0.0.1:9000/items")
    assert any(item["name"] == "ci-monitor" for item in itemcheck.json())
