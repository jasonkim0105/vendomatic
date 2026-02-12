from dataclasses import dataclass
from flask import Flask, request, jsonify, Response
from typing import List

app = Flask(__name__)

coins_inserted: int = 0


def no_body(status: int, headers: dict | None = None) -> Response:
    """Return an empty response with optional headers."""
    resp = Response(status=status)
    if headers:
        for k, v in headers.items():
            resp.headers[k] = str(v)
    return resp

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
  print(coins_inserted)
  return no_body(204)

#DELETE (return isnerted coins)
@app.route("/", methods=['DELETE'])
def delete_coin():
  global coins_inserted
  body = request.get_json()
  coin = body.get("coin")
  while coins_inserted > 0:
     coins_inserted -= coin
  print(coins_inserted)
  return no_body(204)


#GET /inventory
#GET /iventory/:id
#PUT /inventory/:id




if __name__ == "__main__":
  app.run(debug=True)