# vendomatic
Vend-O-Matic project
##Requirements

-Python 3.9+ (Coded in 3.12)
-macOS/Linux/Windows
-pip

## Setup
1. Clone / download repo

2. Create virtual environment
   ```
   python -m venv .venv
   source .venv/bin/activate
   ```   
3. Install Flask
   ```
   pip install Flask
   ```
4. Run Server
   ```
   python main.py
   ```

## Testing

Testing was done via Postman
### Insert Coin
- Insert a coin by making a ``/PUT`` request to ``/``.
- Can only insert one coin at a time
- Body must be in the format: {"coin": 1}
- Anything else will error

### Return Coins
- Return coins by making a ``/DELETE`` request
- Will return all coins that were previously inserted back

### Get Inventory (All Beverages)
- Get inventory by making a ``/GET`` request to ``/inventory``
- Should return back an array of integers matching the quantities of each beverage at the beverage's index

### Get Inventory (Single Beverage)
- Get single beverage inventory number by making a ``/GET`` request to ``/inventory/:beverage_id``
- Should return an integer indicating how much of the specific beverage is left in the vend-o-matic

### Purchase Beverage
- Purchase beverage by making a ``/PUT`` request to ``/inventory/:beverage_id``
- The machine only dispenses 1 beverage per transaction
- Any extra coins in the machine after purchase is returned (shown in response headers)
- Reponse header will also show how many of the beverage is remaining in the invenctory
- Will get 404 error if beverage is out of stock
- Will get 403 error if number of coins is insufficietn
