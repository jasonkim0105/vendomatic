from dataclasses import dataclass
from flask import Flask, request, jsonify, Response
from typing import List

app = Flask(__name__)

coins_inserted: int = 0
inventory = [5] * 3


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




if __name__ == "__main__":
  app.run(debug=True, use_reloader=False)