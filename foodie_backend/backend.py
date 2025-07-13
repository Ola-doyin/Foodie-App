import sys
import os
import random
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from typing import List, Dict, Union
from datetime import datetime
import json

# ==== Setup Paths ====
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Ensure these imports are correct based on your file structure
from foodie_database.original_data import users_db, menu_db, branches_db
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'foodie_database'))

os.makedirs(data_dir, exist_ok=True)

# ==== Utility functions ====
def save_json(filename, data):
    with open(os.path.join(data_dir, filename), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_json(filename):
    # Ensure file exists before trying to load
    filepath = os.path.join(data_dir, filename)
    if not os.path.exists(filepath):
        # Handle case where file doesn't exist, maybe re-run run_once() or return default
        print(f"Warning: {filepath} not found. Re-initializing data.")
        run_once() # Re-initialize if missing
        return load_json(filename) # Try loading again
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

# ==== Run-once initializer ====
def run_once():
    user_path = os.path.join(data_dir, "user.json")
    menu_path = os.path.join(data_dir, "menu.json")
    branches_path = os.path.join(data_dir, "branches.json")

    # Delete old files if they exist to ensure fresh start
    for path in [user_path, menu_path, branches_path]:
        if os.path.exists(path):
            os.remove(path)

    # Write new fresh data
    current_user_key = random.choice(list(users_db.keys()))
    current_user = users_db[current_user_key]
    save_json("user.json", current_user)
    save_json("menu.json", menu_db)
    save_json("branches.json", branches_db)

run_once()

# ==== Load session copies ====

current_user = load_json("user.json")
menu_db = load_json("menu.json")
branches_db = load_json("branches.json") # Fixed: Ensure branches_db is loaded from branches.json

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

class FoodItem(BaseModel):
    name: str
    quantity: int

class OrderItemsRequest(BaseModel):
    items: List[FoodItem]

class PlaceOrderFullRequest(BaseModel):
    items: List[FoodItem]
    total_cost: float
    
class WalletDepositRequest(BaseModel):
    amount: float






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
    raise HTTPException(status_code=404, detail=f"Foodie doesn't have a branch in {location}")


@app.get("/pre_book/{location}/{table_type}")
async def pre_booking(location: str, table_type: str):
    location_lower = location.lower()
    if location_lower not in branches_db:
        raise HTTPException(status_code=404, detail=f"Foodie doesn't have a branch in {location}")

    tables = branches_db[location_lower]["available_tables"]
    if table_type not in tables:
        raise HTTPException(status_code=404, detail="Table type not available at this branch.")

    if tables[table_type]["number"] <= 0:
        raise HTTPException(status_code=400, detail="No tables available for this type at this branch.")
    
    # Calculate estimated cost
    price = tables[table_type]["unit_price"]

    return {
        "message": f"Provisional summary for booking a '{table_type}' at {location.title()} branch:",
        "table_type": table_type,
        "location": location.title(),
        "estimated_cost": price,
        "currency": "Naira",
        "availability": tables[table_type]["number"] > 0
    }


@app.post("/book_table/")
async def book_table(location: str, table_type: str):
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


@app.post("/pre_order/")
async def pre_order(request: OrderItemsRequest):
    total = 0
    price_lookup = {
        item["name"]: item["price"]
        for section in menu_db.values() if isinstance(section, list)
        for item in section
    }

    unavailable_items = []
    summary_items = []

    for food_item in request.items:
        name = food_item.name
        quantity = food_item.quantity

        if name not in price_lookup:
            unavailable_items.append(name)
        else:
            unit_price = price_lookup[name]
            subtotal = unit_price * quantity
            total += subtotal
            summary_items.append({
                "item": name,
                "quantity": quantity,
                "unit_price": unit_price,
                "subtotal": round(subtotal, 2)
            })

    if unavailable_items:
        raise HTTPException(status_code=400, detail=f"The following food items are not found in the menu: {', '.join(unavailable_items)}")

    vat_percentage = menu_db.get("settings", {}).get("vat_percentage", 0)
    vat_amount = (vat_percentage / 100) * total
    grand_total = total + vat_amount

    return {
        "message": "Provisional order summary:",
        "ordered_items": summary_items,
        "sub_total": round(total, 2),
        "vat_percentage": vat_percentage,
        "vat_amount": round(vat_amount, 2),
        "grand_total": round(grand_total, 2),
        "currency": "Naira"
    }


@app.post("/place_order/")
async def place_order(request:PlaceOrderFullRequest):
    total = 0
    price_lookup = {
        item["name"]: item["price"]
        for section in menu_db.values() if isinstance(section, list)
        for item in section
    }

    unavailable_items = []
    for food_item in request.items:
        name = food_item.name
        quantity = food_item.quantity

        if name not in price_lookup:
            unavailable_items.append(name)
        else:
            total += price_lookup[name] * quantity

    if unavailable_items:
        raise HTTPException(status_code=400, detail=f"Unavailable items: {', '.join(unavailable_items)}")

    vat_percentage = menu_db.get("settings", {}).get("vat_percentage", 0)
    vat = (vat_percentage / 100) * total
    grand_total = total + vat

    # ⚠️ Validate frontend total
    if abs(grand_total - request.total_cost) > 1e-2:
        raise HTTPException(status_code=400, detail="Mismatch in total cost submitted.")

    if current_user["wallet_balance"] < grand_total:
        raise HTTPException(status_code=400, detail="Insufficient wallet balance.")

    current_user["wallet_balance"] -= grand_total

    now = datetime.now()
    current_user["last_orders"].insert(0, {
        "food": [food_item.dict() for food_item in request.items],
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M")
    })

    save_json("user.json", current_user)

    return {
        "message": "Order placed successfully",
        "ordered_items": [item.dict() for item in request.items],
        "sub_total": round(total, 2),
        "vat": round(vat, 2),
        "grand_total": round(grand_total, 2),
        "new_wallet_balance": round(current_user["wallet_balance"], 2)
    }


# NEW: wallet_deposit Endpoint
@app.post("/wallet_deposit/")
async def wallet_deposit(request: WalletDepositRequest):
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="Deposit amount must be positive.")
    
    current_user["wallet_balance"] += request.amount
    save_json("user.json", current_user)

    return {
        "message": f"Successfully deposited ₦{request.amount:.2f} to your wallet.",
        "new_wallet_balance": round(current_user["wallet_balance"], 2)
    }

# restart_server Endpoint
@app.post("/admin/reset")
def manual_reset():
    global current_user, menu_db, branches_db
    run_once()
    current_user = load_json("user.json")
    menu_db = load_json("menu.json")
    branches_db = load_json("branches.json")
    return {"message": "Data has been reset"}



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