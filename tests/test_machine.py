import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))
import main

#reset the global variables before each test
@pytest.fixture(autouse=True)
def reset_state():
    with main.lock:
        main.coins_inserted = 0
        main.inventory[:] = [5, 5, 5]


@pytest.fixture()
def client():
    main.app.config["TESTING"] = True
    with main.app.test_client() as test_client:
        yield test_client


def put_coin(client, n = 1):
    last = None
    for _ in range(n):
        last = client.put("/", json={"coin": 1})
    return last


#test /PUT request to insert single coin
def test_put_coins(client):
    r1 = client.put("/", json={"coin": 1})
    assert r1.status_code == 204
    assert r1.headers.get("X-Coins") == "1"

def test_put_invalid_coin(client):
    r = client.put("/", json={"coin": 2})
    assert r.status_code == 400
    assert "error" in r.get_json()

#test /DELETE
def test_delete_coins_and_resets(client):
    put_coin(client, 2)

    r = client.delete("/")
    assert r.status_code == 204
    assert r.headers.get("X-Coins") == "2"

#test /GET inventory
def test_get_inventory_returns_array(client):
    r = client.get("/inventory")
    assert r.status_code == 200
    assert r.get_json() == [5, 5, 5]

#should show 200 success code and show inventory of 5
def test_get_inventory_id_returns_int(client):
    r = client.get("/inventory/1")
    assert r.status_code == 200
    assert r.get_json() == 5

#should show 404 error code
def test_get_inventory_invalid_id(client):
    r = client.get("/inventory/999")
    assert r.status_code == 404

#should show 403 when none of 1 coin inserted
def test_put_inventory_insufficent_403(client):
    r0 = client.put("/inventory/1")
    assert r0.status_code == 403
    assert r0.headers.get("X-Coins") == "0"

    put_coin(client, 1)
    r1 = client.put("/inventory/1")
    assert r1.status_code == 403
    assert r1.headers.get("X-Coins") == "1"

#should show 404 when inventory is oos
def test_put_inventory_oos_404(client):
    with main.lock:
        main.inventory[0] = 0

    put_coin(client, 2)

    r = client.put("/inventory/1")
    assert r.status_code == 404
    assert r.headers.get("X-Coins") == "2"

#should get 200 success and dispense one beverage
def test_put_inventory_success_200(client):
    put_coin(client, 3)

    r = client.put("/inventory/1")
    assert r.status_code == 200
    assert r.get_json() == {"quantity": 1}
    assert r.headers.get("X-Coins") == "1"
    assert r.headers.get("X-Inventory-Remaining") == "4"
