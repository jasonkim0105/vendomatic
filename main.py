from flask import Flask, request, jsonify, Response
import threading

app = Flask(__name__)

lock = threading.Lock()
coins_inserted: int = 0
inventory = [5, 5, 5]

PRICE = 2
BEVERAGE_COUNT = 3

@app.route("/")
def home():
  return "Home"

#PUT with body {"coin": 1}
@app.route("/", methods=["PUT"])
def insert_coin():
  global coins_inserted
  body = request.get_json()
  coin = body.get("coin")

  if coin != 1:
    return jsonify({"error": 'Body must be {"coin": 1}'}), 400

  with lock:
    coins_inserted += coin

  resp = Response(status=204)
  resp.headers["X-Coins"] = str(coins_inserted)
  return resp

#DELETE (remove all coins)
@app.route("/", methods=["DELETE"])
def delete_coin():
  global coins_inserted

  with lock:
    coins_returned = coins_inserted
    coins_inserted = 0

  resp = Response(status=204)
  resp.headers["X-Coins"] = str(coins_returned)
  return resp


#GET /coins (return inserted coins. not required)
@app.route("/coins", methods=["GET"])
def get_coins():
   global coins_inserted
   with lock:
     return jsonify(coins_inserted), 200

#GET /inventory (as an array of integers)
@app.route("/inventory", methods=["GET"])
def get_inventory():
  global inventory
  with lock:
    return jsonify(list(inventory)), 200

#GET /iventory/:id
@app.route("/inventory/<int:beverage_id>", methods=["GET"])
def get_inventory_id(beverage_id: int):
  if not (1 <= beverage_id <= BEVERAGE_COUNT):
    return Response(status=404)

  with lock:
    return jsonify(inventory[beverage_id - 1]), 200

#PUT /inventory/:id
@app.route("/inventory/<int:beverage_id>", methods=["PUT"])
def put_inventory_purchase(beverage_id: int):
  global coins_inserted, inventory

  if not (1 <= beverage_id <= BEVERAGE_COUNT):
    return Response(status=404)

  idx = beverage_id - 1

  #return 403 if not enough coins inserted
  with lock:
    if coins_inserted < PRICE:
      resp = Response(status=403)
      resp.headers["X-Coins"] = "0"
      return resp


    #return 404 if inventory is at 0 of particular beverage
    if inventory[idx] < 1:
      resp = Response(status=404)
      resp.headers["X-Coins"] = str(coins_inserted)
      return resp

    #return 200 if possible to buy beverage
    can_buy = coins_inserted // PRICE
    beverages_vended = min(can_buy, inventory[idx])
    change = coins_inserted - (beverages_vended * PRICE)
    inventory[idx] -= beverages_vended
    coins_inserted = 0

    resp = jsonify({"quantity": beverages_vended})
    resp.headers["X-Coins"] = str(change)
    resp.headers["X-Inventory-Remaining"] = str(inventory[idx])
    return resp


if __name__ == "__main__":
  app.run(debug=True, use_reloader=False)