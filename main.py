from flask import Flask, request, jsonify, Response
from typing import List

app = Flask(__name__)

coins_inserted: int = 0
inventory = [5, 5, 5]
price = 2


@app.route("/")
def home():
  return "Home"

#PUT with body {"coin": 1}
@app.route("/", methods=['PUT'])
def insert_coin():
  global coins_inserted
  body = request.get_json()
  coin = body.get("coin")
  coins_inserted += coin

  resp = Response(status=204)
  resp.headers["X-Coins"] = str(coins_inserted)
  return resp

#DELETE (remove all coins)
@app.route("/", methods=['DELETE'])
def delete_coin():
  global coins_inserted
  coins_inserted = 0
  resp = Response(status=204)
  resp.headers["X-Coins"] = str(coins_inserted)
  return resp


#GET /coins (return inserted coins)
@app.route("/coins", methods=['GET'])
def get_coins():
   global coins_inserted
   return jsonify(coins_inserted), 200

#GET /inventory (as an array of integers)
@app.route("/inventory", methods=["GET"])
def get_inventory():
  global inventory
  return jsonify(list(inventory))

#GET /iventory/:id
@app.route("/inventory/<int:beverage_id>", methods=["GET"])
def get_inventory_id(beverage_id: int):
  return jsonify(inventory[beverage_id - 1]), 200

#PUT /inventory/:id
@app.route("/inventory/<int:beverage_id>", methods=["PUT"])
def put_inventory_purchase(beverage_id: int):
  global coins_inserted, inventory

  #return 403 if not enough coins inserted
  if coins_inserted < price:
    resp = Response(status=403)
    resp.headers["X-Coins"] = "0"
    return resp

  idx = beverage_id - 1

  #return 404 if inventory is at 0 of particular beverage
  if inventory[idx] < 1:
    resp = Response(status=404)
    resp.headers["X-Coins"] = str(coins_inserted)
    return resp

  #return 200 if possible to buy beverage
  can_buy = coins_inserted // price
  beverages_vended = min(can_buy, inventory[idx])
  change = coins_inserted - (beverages_vended * price)
  inventory[idx] -= beverages_vended
  coins_inserted = 0

  resp = Response(status=200)
  resp.headers["X-Coins"] = str(change)
  resp.headers["X-Inventory-Remaining"] = str(inventory[idx])
  return resp


if __name__ == "__main__":
  app.run(debug=True, use_reloader=False)