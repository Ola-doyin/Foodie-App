import os
import json
import requests # Make sure 'requests' library is installed (pip install requests)
from google import genai
from google.genai.types import FunctionDeclaration


# === CONFIGURATION ===
FASTAPI_BASE_URL = "https://foodie-backend-mq80.onrender.com" # Your FastAPI backend


# === TOOL DISPATCHER ===
def call_fastapi_endpoint(function_name: str, **kwargs):
    """
    Dispatches function calls to the appropriate FastAPI backend endpoint.
    """
    routes = {
        "get_current_user_info_api": lambda: requests.get(f"{FASTAPI_BASE_URL}/user"),
        "get_user_wallet_balance_api": lambda: requests.get(f"{FASTAPI_BASE_URL}/user/wallet"),
        "get_user_last_orders_api": lambda: requests.get(f"{FASTAPI_BASE_URL}/user/orders"),
        "get_full_menu_api": lambda: requests.get(f"{FASTAPI_BASE_URL}/menu"),
        "get_menu_category_api": lambda: requests.get(f"{FASTAPI_BASE_URL}/menu/{kwargs['category']}"),
        "list_all_branches_api": lambda: requests.get(f"{FASTAPI_BASE_URL}/branches"),
        "get_branch_details_api": lambda: requests.get(f"{FASTAPI_BASE_URL}/branches/{kwargs['location']}"),
        "pre_booking_api": lambda: requests.get(f"{FASTAPI_BASE_URL}/pre_book/{kwargs['location']}/{kwargs['table_type']}"), 
        "book_table_api": lambda: requests.post(f"{FASTAPI_BASE_URL}/book_table/", params={
            "location": kwargs["location"],
            "table_type": kwargs["table_type"]
        }),
        "pre_order_api": lambda: requests.post(f"{FASTAPI_BASE_URL}/pre_order/", json={
            "items": kwargs["items"]  # List of {"name": ..., "quantity": ...}
        }
        ),
        "place_order_api": lambda: requests.post(f"{FASTAPI_BASE_URL}/place_order/", json={
            "items": kwargs["items"],            # Same structure as pre_order
            "total_cost": kwargs["total_cost"]   # float value
        }),

    }

    if function_name not in routes:
        raise ValueError(f"Unknown function: {function_name}")

    response = routes[function_name]()
    response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
    return response.json()


# === GEMINI TOOL DECLARATIONS ===
restaurant_tools = [
    FunctionDeclaration(
        name="get_current_user_info_api",
        description="Get current user's profile info (ID, wallet balance in naira, last orders).",
        parameters={},
    ),
    FunctionDeclaration(
        name="get_user_wallet_balance_api",
        description="Get current user's wallet balance in naira.",
        parameters={},
    ),
    FunctionDeclaration(
        name="get_user_last_orders_api",
        description="Get last food orders by the user.",
        parameters={},
    ),
    FunctionDeclaration(
        name="get_full_menu_api",
        description="Get the full categorized menu and prices in naira.",
        parameters={},
    ),
    FunctionDeclaration(
        name="get_menu_category_api",
        description="Briefly list with their prices in naira all menu item in the given category (e.g., 'soups', 'sides')",
        parameters={
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "The category of menu items, e.g., 'soups', 'sides', 'main_courses'."
                }
            },
            "required": ["category"],
        },
    ),
    FunctionDeclaration(
        name="list_all_branches_api",
        description="List all restaurant branches.",
        parameters={},
    ),
    FunctionDeclaration(
        name="get_branch_details_api",
        description="Get details of a branch (available tables, specials, hours, manager, contact, delivery availability, operating hours.",
        parameters={
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location name of the branch, e.g., 'Victoria Island', 'Ikeja'."
                }
            },
            "required": ["location"],
        },
    ),
    
    FunctionDeclaration(
        name="pre_booking_api",
        description=(
            "**BEFORE USER'S CONFIRMATION** Provides a provisional summary or invoice for a requested table booking. **It returns a summary/provisional invoice for user review and does not process booking or deduct wallet**"
        ),
        parameters={
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location name of the branch for the provisional booking (e.g., 'Ikeja', 'Victoria Island')."
                },
                "table_type": {
                    "type": "string",
                    "description": "The type of table to book, e.g., 'table_for_2', 'table_for_3', 'VIP table', etc."
                }
            },
            "required": ["location", "table_type"],
        },
    ),
    FunctionDeclaration(
        name="book_table_api",
        description=(
            """**AFTER USER'S CONFIRMATION**, Book a table at a Foodie branch, remove the amount from wallet, and subtract that table from available tables. 
            This tool finalizes a table booking and processes payment **based solely on the provided branch location and table type**. """
        ),
        parameters={
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location name of the branch where the table is to be booked."
                },
                "table_type": {
                    "type": "string",
                    "description": "The type of table to book, e.g., 'table_for_2', 'table_for_3', 'VIP table', etc."
                }
            },
            "required": ["location", "table_type"],
        },
    ),
    FunctionDeclaration(
        name="pre_order_api",
        description="**BEFORE USER'S CONFIRMATION**, Gives a provisional summary or invoice for a requested food order with quantities. **This does NOT place the order or deduct money.**",
        parameters={
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "quantity": {"type": "integer", "minimum": 1}
                        },
                        "required": ["name", "quantity"]
                    },
                    "description": "A list of food items with quantities, e.g., [{\"name\": \"Jollof Rice\", \"quantity\": 2}]"
                }
            },
            "required": ["items"],
        },
    ),
    FunctionDeclaration(
        name="place_order_api",
        description="**AFTER USER'S CONFIRMATION**, Place a food order (deducts total from wallet), adds order to last orders, generates receipt.",
        parameters={
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "quantity": {"type": "integer", "minimum": 1}
                        },
                        "required": ["name", "quantity"]
                    },
                    "description": "A list of food items with quantities, e.g., [{\"name\": \"Jollof Rice\", \"quantity\": 2}]"
                },
                "total_cost": { 
                    "type": "number",
                    "description": "The final total cost of the order to be deducted from the user's wallet. Must match the confirmed pre_order value."
                }
            },
            "required": ["items", "total_cost"], 
        },
    )
]


__all__ = ["restaurant_tools", "call_fastapi_endpoint"]