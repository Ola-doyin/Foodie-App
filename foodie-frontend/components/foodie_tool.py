import os
import json
import requests
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
        "book_table_api": lambda: requests.post(f"{FASTAPI_BASE_URL}/book_table/", params={
            "location": kwargs["location"],
            "table_type": kwargs["table_type"]
        }),
        "place_order_api": lambda: requests.post(f"{FASTAPI_BASE_URL}/place_order/", json=kwargs["items"]),
    }

    if function_name not in routes:
        raise ValueError(f"Unknown function: {function_name}")

    response = routes[function_name]()
    response.raise_for_status()
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
        description="Get details of a branch (avaialble tables(vip, table for 2, table for 4, etcgit), specials, hours, etc).",
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
        name="book_table_api",
        description="Book a table at a branch, remove the amount from wallet, and subtract that table from available tables.",
        parameters={
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location name of the branch where the table is to be booked."
                },
                "table_type": {
                    "type": "string",
                    "description": "The type of table to book, e.g., 'table_for_2', 'table_for_3', 'table_for_5', 'table_for_8', 'vip'."
                }
            },
            "required": ["location", "table_type"],
        },
    ),
    FunctionDeclaration(
        name="place_order_api",
        description="Place a food order (deducts total from wallet), adds order to last orders, generates invoice.",
        parameters={
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "A list of food items to order, e.g., ['Jollof Rice', 'Chicken Wings']."
                }
            },
            "required": ["items"],
        },
    ),
]


__all__ = ["restaurant_tools", "call_fastapi_endpoint"]