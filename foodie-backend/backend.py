import sys
import os
import random
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
import json

# ==== Setup Paths ====
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from foodie_database.original_data import users_db, menu_db, branches_db
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'foodie_database'))
os.makedirs(data_dir, exist_ok=True)

# ==== Utility functions ====
def save_json(filename, data):
    with open(os.path.join(data_dir, filename), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_json(filename):
    with open(os.path.join(data_dir, filename), "r", encoding="utf-8") as f:
        return json.load(f)

# ==== Run-once initializer ====
def run_once():
    user_path = os.path.join(data_dir, "user.json")
    menu_path = os.path.join(data_dir, "menu.json")
    branches_path = os.path.join(data_dir, "branches.json")

    # Delete old files if they exist
    for path in [user_path, menu_path, branches_path]:
        if os.path.exists(path):
            os.remove(path)

    # Write new fresh data
    current_user_key = random.choice(list(users_db.keys()))
    current_user = users_db[current_user_key]
    save_json("user.json", current_user)
    save_json("menu.json", menu_db)
    save_json("branches.json", branches_db)

# ==== Run it ====
run_once()

# ==== Load session copies ====
current_user  = load_json("user.json")
menu_db       = load_json("menu.json")
branches_db   = load_json("branches.json")

# ==== FastAPI App ====
app = FastAPI(title="FoodieBot Backend API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==== Models ====
class OrderItem(BaseModel):
    food: List[str]
    date: str
    time: str

class User(BaseModel):
    customer_id: int
    wallet_balance: float
    last_orders: List[OrderItem]

class MenuItem(BaseModel):
    name: str
    price: float

class TableInfo(BaseModel):
    number: int
    unit_price: float

class BranchSpecial(BaseModel):
    day: str
    food: List[str]
    discount: float

class BranchInfo(BaseModel):
    location: str
    available_tables: Dict[str, TableInfo]
    specials: List[BranchSpecial]
    opening_hours: Dict[str, str]
    contact_number: str
    delivery_available: bool
    rating: float
    manager: str

# ==== Endpoints ====

@app.get("/")
def root():
    return {
        "message": f"Welcome Foodie_0{current_user['customer_id']}, your wallet balance is ₦{current_user['wallet_balance']:.2f}"
    }

@app.get("/user", response_model=User)
def get_current_user():
    return current_user

@app.get("/user/wallet")
def get_wallet_balance():
    return {"wallet_balance": current_user["wallet_balance"]}

@app.get("/user/orders")
def get_last_orders():
    return current_user["last_orders"]

@app.get("/menu")
def get_full_menu():
    return menu_db

@app.get("/menu/{category}")
def get_menu_category(category: str):
    if category in menu_db:
        return menu_db[category]
    raise HTTPException(status_code=404, detail="Category not found")

@app.get("/branches")
def list_all_branches():
    return list(branches_db.keys())

@app.get("/branches/{location}", response_model=BranchInfo)
def get_branch_details(location: str):
    location = location.lower()
    if location in branches_db:
        return branches_db[location]
    raise HTTPException(status_code=404, detail="Branch not found")

@app.post("/book_table/")
def book_table(location: str, table_type: str):
    location = location.lower()
    if location not in branches_db:
        raise HTTPException(status_code=404, detail="Branch not found")

    tables = branches_db[location]["available_tables"]
    if table_type not in tables:
        raise HTTPException(status_code=404, detail="Table type not available")

    if tables[table_type]["number"] <= 0:
        raise HTTPException(status_code=400, detail="No tables available for this type")

    price = tables[table_type]["unit_price"]
    if current_user["wallet_balance"] < price:
        raise HTTPException(status_code=400, detail="Insufficient wallet balance to book this table.")

    tables[table_type]["number"] -= 1
    current_user["wallet_balance"] -= price

    save_json("user.json", current_user)
    save_json("branches.json", branches_db)

    return {
        "message": f"Table '{table_type}' booked at {location.title()} branch.",
        "paid": price,
        "remaining_tables": tables[table_type]["number"],
        "new_wallet_balance": round(current_user["wallet_balance"], 2)
    }

@app.post("/place_order/")
def place_order(items: List[str]):
    total = 0
    price_lookup = {
        item["name"]: item["price"]
        for section in menu_db.values() if isinstance(section, list)
        for item in section
    }

    for food in items:
        if food not in price_lookup:
            raise HTTPException(status_code=400, detail=f"Food item '{food}' not found in menu.")
        total += price_lookup[food]

    vat = menu_db["settings"]["vat_percentage"] / 100 * total
    grand_total = total + vat

    if current_user["wallet_balance"] < grand_total:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    current_user["wallet_balance"] -= grand_total

    now = datetime.now()
    new_order = {
        "food": items,
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M")
    }
    current_user["last_orders"].insert(0, new_order)

    save_json("user.json", current_user)

    return {
        "message": "Order placed successfully",
        "ordered_items": items,
        "total": round(total, 2),
        "vat": round(vat, 2),
        "grand_total": round(grand_total, 2),
        "new_wallet_balance": round(current_user["wallet_balance"], 2)
    }

# ==== Dev Server ====
if __name__ == "__main__":
    def is_port_in_use(host="127.0.0.1", port=8000):
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex((host, port)) == 0

    if not is_port_in_use():
        print("[Starting FastAPI Backend on port 8000]")
        uvicorn.run("components.backend:app", host="127.0.0.1", port=8000, reload=False)
    else:
        print("[Backend already running on port 8000]")
