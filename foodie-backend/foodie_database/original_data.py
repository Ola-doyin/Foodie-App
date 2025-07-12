# FoodieDatabase.py
# This is a sample database just to illustrate how the Foodie AI assistant can access user and menu data.

from datetime import datetime

# Registered users and their details
users_db = {
    "user_01": {
        "customer_id": 1,
        "wallet_balance": 26005.00,
        "last_orders": [
            {"food": ["Jollof Rice", "Chicken", "Plantain"], "date": "2025-07-10", "time": "13:45"},
            {"food": ["Pounded Yam", "Egusi", "Goat Meat"], "date": "2025-07-09", "time": "14:30"},
            {"food": ["Fried Yam", "Peppered Chicken"], "date": "2025-07-08", "time": "11:15"},
            {"food": ["Village Rice", "Fish Sauce"], "date": "2025-07-07", "time": "15:10"},
            {"food": ["Rice And Beans", "Gizz Dodo", "Zobo Drink"], "date": "2025-07-06", "time": "18:20"},
            {"food": ["Chapman"], "date": "2025-07-05", "time": "10:00"},
        ]
    },
    "user_02": {
        "customer_id": 2,
        "wallet_balance": 3700.00,
        "last_orders": [
            {"food": ["Ofada Rice/Sauce", "Boiled Egg", "Palmwine"], "date": "2025-07-09", "time": "12:10"},
            {"food": ["Ofada Rice/Sauce", "Boiled Egg"], "date": "2025-07-06", "time": "12:50"},
            {"food": ["Amala", "Ewedu", "Gbegiri", "Assorted"], "date": "2025-07-05", "time": "14:00"},
            {"food": ["White Rice", "Moi Moi", "Fried Potatoes"], "date": "2025-07-02", "time": "17:40"},
        ]
    },
    "user_03": {
        "customer_id": 3,
        "wallet_balance": 13904.00,
        "last_orders": [
            {"food": ["Spaghetti Jollof", "Egg Sauce"], "date": "2025-07-10", "time": "19:10"},
            {"food": ["Yam Porridge", "Fried Plantain"], "date": "2025-07-09", "time": "19:10"},
            {"food": ["Ewa Agoyin", "Chicken (Small)", "Zobo Drink"], "date": "2025-07-06", "time": "09:50"},
            {"food": ["Semovita", "Ogbono", "Ponmo"], "date": "2025-07-05", "time": "14:30"},
            {"food": ["Fruit Salad", "Puff Puff"], "date": "2025-07-04", "time": "10:20"},
            {"food": ["Boiled Yam", "Catfish Pepper Soup"], "date": "2025-07-03", "time": "18:30"},
        ]
    },
    "user_04": {
        "customer_id": 4,
        "wallet_balance": 18003.00,
        "last_orders": [
            {"food": ["Eba", "Edikaikong", "Cow Leg"], "date": "2025-07-10", "time": "13:15"},
            {"food": ["Special Fried Rice", "Turkey (Small)", "Milk Shake"], "date": "2025-07-09", "time": "16:00"},
            {"food": ["Boiled Plantain", "Egg Sauce", "Shrimps"], "date": "2025-07-08", "time": "20:00"},
        ]
    },
    "user_05": {
        "customer_id": 5,
        "wallet_balance": 35700.70,
        "last_orders": [
            {"food": ["Fried Rice", "Moi Moi", "Croaker Fish"], "date": "2025-07-10", "time": "14:00"},
            {"food": ["Semovita", "Seafood Okro"], "date": "2025-07-09", "time": "15:40"},
            {"food": ["Akara", "Cooked Pap"], "date": "2025-07-08", "time": "07:30"},
            {"food": ["Dodo Gizzard", "Boiled Yam", "Zobo Drink"], "date": "2025-07-07", "time": "12:10"},
            {"food": ["Palmwine"], "date": "2025-07-06", "time": "18:20"},
            {"food": ["Ogbono", "Goat Meat", "Water"], "date": "2025-07-05", "time": "14:50"},
            {"food": ["Catfish Pepper Soup", "Pounded Yam"], "date": "2025-07-04", "time": "20:10"},
        ]
    },
    "user_06": {
        "customer_id": 6,
        "wallet_balance": 7910.00,
        "last_orders": [
            {"food": ["Fruit Salad", "Milk Shake"], "date": "2025-07-10", "time": "11:45"},
        ]
    }
}


menu_db = {
    "sides": [
        {"name": "Puff Puff", "price": 400},
        {"name": "Fried Yam", "price": 400},
        {"name": "Fried Potatoes", "price": 400},
        {"name": "Fruit Salad", "price": 500},
        {"name": "Akara", "price": 500},
        {"name": "Cooked Pap", "price": 300},
        {"name": "Peppered Ponmo", "price": 250},
        {"name": "Peppered Chicken", "price": 850},
        {"name": "Round Panla", "price": 600},
        {"name": "Shrimps", "price": 1200}
    ],
    
    "main_menu": [
        {"name": "Jollof Rice", "price": 900},
        {"name": "Village Rice", "price": 1000},
        {"name": "Ofada Rice/Sauce", "price": 1700},
        {"name": "Coconut Rice", "price": 1200},
        {"name": "White Rice", "price": 800},
        {"name": "Rice And Beans", "price": 800},
        {"name": "Special Fried Rice", "price": 1200},
        {"name": "Ewa Agoyin", "price": 600},
        {"name": "Beans Porridge", "price": 500},
        {"name": "Yam Porridge", "price": 700},
        {"name": "Boiled Yam", "price": 500},
        {"name": "Spaghetti Jollof", "price": 700},
        {"name": "Farm House Porridge", "price": 800}
    ],
    
    "soups": [
        {"name": "Egusi", "price": 900},
        {"name": "Efo Riro", "price": 900},
        {"name": "Edikaikong", "price": 900},
        {"name": "Afang", "price": 900},
        {"name": "Ogbono", "price": 900},
        {"name": "Ewedu", "price": 100},
        {"name": "Gbegiri", "price": 100},
        {"name": "Catfish Pepper Soup", "price": 1000},
        {"name": "Bitter Leaf Soup", "price": 900},
        {"name": "Seafood Okro", "price": 3500},
        {"name": "White Soup", "price": 1500},
        {"name": "Oha Soup", "price": 900}
    ],

    "proteins": [
        {"name": "Hake Fish", "price": 1200},
        {"name": "Titus", "price": 1000},
        {"name": "Turkey (Big)", "price": 2000},
        {"name": "Turkey (Small)", "price": 1200},
        {"name": "Chicken", "price": 1700},
        {"name": "Chicken (Small)", "price": 850},
        {"name": "Cow Leg", "price": 1000},
        {"name": "Goat Meat", "price": 1500},
        {"name": "Beef", "price": 700},
        {"name": "Assorted", "price": 500},
        {"name": "Ponmo", "price": 500},
        {"name": "Panla", "price": 600},
        {"name": "Boiled Egg", "price": 250},
        {"name": "Croaker Fish", "price": 2000},
        {"name": "Roasted Cat Fish", "price": 2000}
    ],
    
    "swallows": [
        {"name": "Amala", "price": 500},
        {"name": "Pounded Yam", "price": 400},
        {"name": "Semo", "price": 300},
        {"name": "Eba", "price": 200}
    ],
    
    "extras": [
        {"name": "Plantain", "price": 500},
        {"name": "Egg Sauce", "price": 500},
        {"name": "Moi Moi", "price": 500},
        {"name": "Fish Sauce", "price": 1000},
        {"name": "Boiled Plantain", "price": 900},
        {"name": "Gizz Dodo", "price": 900},
        {"name": "Ofada Sauce", "price": 900}
    ],

    "drinks": [
        {"name": "Palmwine", "price": 700},
        {"name": "Zobo Drink", "price": 500},
        {"name": "Chapman", "price": 700},
        {"name": "Soda", "price": 400},
        {"name": "Milk Shake", "price": 800},
        {"name": "Apple Juice", "price": 700},
        {"name": "Blackcurrant Juice", "price": 600},
        {"name": "Caprison", "price": 300},
        {"name": "Malt", "price": 500},
        {"name": "Water", "price": 200}
    ],
    
    "settings": {
        "takeaway_pack_price": 500,
        "vat_percentage": 7.5
    }
}


branches_db = {
    "ikorodu": {
        "location": "Ikorodu",
        "available_tables": {
            "table_for_2": {"number": 4, "unit_price": 6800},
            "table_for_5": {"number": 2, "unit_price": 10350},
            "vip": {"number": 1, "unit_price": 15800}
        },
        "specials": [
            {"day": "Monday", "food": ["Ofada Rice/Sauce", "Pepper Soup"], "discount": 10},
            {"day": "Wednesday", "food": ["Yam Porridge", "Turkey (Big)"], "discount": 12},
            {"day": "Friday", "food": ["Jollof Rice", "Croaker Fish"], "discount": 15}
        ],
        "opening_hours": {
            "weekday": "08:00 - 21:00",
            "weekend": "09:00 - 22:00"
        },
        "contact_number": "+234-701-234-5678",
        "delivery_available": True,
        "rating": 4.2,
        "manager": "Mrs. Adebayo"
    },

    "ikeja": {
        "location": "Ikeja",
        "available_tables": {
            "table_for_2": {"number": 6, "unit_price": 7600},
            "table_for_5": {"number": 4, "unit_price": 12300},
            "vip": {"number": 3, "unit_price": 18500}
        },
        "specials": [
            {"day": "Tuesday", "food": ["Pounded Yam", "Egusi", "Goat Meat"], "discount": 13},
            {"day": "Thursday", "food": ["Fried Rice", "Shrimps"], "discount": 10},
            {"day": "Saturday", "food": ["Spaghetti Jollof", "Turkey (Small)"], "discount": 12}
        ],
        "opening_hours": {
            "weekday": "08:00 - 21:00",
            "weekend": "09:00 - 22:00"
        },
        "contact_number": "+234-802-987-6543",
        "delivery_available": True,
        "rating": 4.7,
        "manager": "Mr. Okoro"
    },

    "epe": {
        "location": "Epe",
        "available_tables": {
            "table_for_2": {"number": 3, "unit_price": 6000},
            "table_for_5": {"number": 2, "unit_price": 12800},
            "vip": {"number": 1, "unit_price": 16500}
        },
        "specials": [
            {"day": "Monday", "food": ["Boiled Yam", "Efo Riro"], "discount": 8},
            {"day": "Wednesday", "food": ["White Rice", "Fish Sauce"], "discount": 10},
            {"day": "Sunday", "food": ["Catfish Pepper Soup", "Akara"], "discount": 12}
        ],
        "opening_hours": {
            "weekday": "09:00 - 20:00",
            "weekend": "10:00 - 22:00"
        },
        "contact_number": "+234-909-111-2222",
        "delivery_available": False,
        "rating": 4.0,
        "manager": "Mrs. Fatima"
    },

    "badagry": {
        "location": "Badagry",
        "available_tables": {
            "table_for_3": {"number": 5, "unit_price": 4700},
            "table_for_8": {"number": 3, "unit_price": 9300},
            "vip": {"number": 2, "unit_price": 14800}
        },
        "specials": [
            {"day": "Tuesday", "food": ["Ewa Agoyin", "Fried Plantain"], "discount": 10},
            {"day": "Thursday", "food": ["Village Rice", "Titus"], "discount": 14},
            {"day": "Saturday", "food": ["Farm House Porridge", "Palmwine"], "discount": 11}
        ],
        "opening_hours": {
            "weekday": "08:00 - 20:00",
            "weekend": "09:00 - 21:00"
        },
        "contact_number": "+234-703-333-4444",
        "delivery_available": True,
        "rating": 4.3,
        "manager": "Mr. Danjuma"
    },

    "victoria_island": {
        "location": "Victoria Island",
        "available_tables": {
            "table_for_2": {"number": 7, "unit_price": 7500},
            "table_for_4": {"number": 5, "unit_price": 13800},
            "vip": {"number": 4, "unit_price": 20000}
        },
        "specials": [
            {"day": "Wednesday", "food": ["Special Fried Rice", "Prawns"], "discount": 13},
            {"day": "Friday", "food": ["Ofada Sauce", "Boiled Plantain"], "discount": 12},
            {"day": "Sunday", "food": ["Seafood Okro", "Chapman"], "discount": 15}
        ],
        "opening_hours": {
            "weekday": "08:00 - 22:00",
            "weekend": "09:00 - 23:00"
        },
        "contact_number": "+234-805-999-8888",
        "delivery_available": True,
        "rating": 4.8,
        "manager": "Ms. Uduak"
    },

    "yaba": {
        "location": "Yaba",
        "available_tables": {
            "table_for_3": {"number": 4, "unit_price": 6000},
            "table_for_5": {"number": 2, "unit_price": 10300},
            "vip": {"number": 1, "unit_price": 15000}
        },
        "specials": [
            {"day": "Monday", "food": ["Beans Porridge", "Ponmo"], "discount": 9},
            {"day": "Thursday", "food": ["Amala", "Gbegiri", "Ewedu"], "discount": 13},
            {"day": "Saturday", "food": ["White Soup", "Goat Meat"], "discount": 14}
        ],
        "opening_hours": {
            "weekday": "08:00 - 21:00",
            "weekend": "09:00 - 22:00"
        },
        "contact_number": "+234-814-456-1234",
        "delivery_available": True,
        "rating": 4.4,
        "manager": "Mr. Tunde"
    }
}
