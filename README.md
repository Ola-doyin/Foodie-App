# 🍲 Foodie Web App

**Foodie-App** is a smart, image-aware, multilingual **web chatbot** customized for the **Foodie Restaurant** food chain in Lagos, Nigeria. It helps users explore the world of food, discover delicacies, and seamlessly patronize the Foodie Restaurant.

Powered by a **Streamlit frontend**, a **FastAPI backend**, and **Google Gemini Pro**, Foodie-App delivers delightful and intelligent food conversations — including image-based queries, menu browsing, table booking, and order placement.


<br>


## 🚀 Deployment for Use
You can use Foodie Web App in two ways: locally or via the deployed links.
⚠️ **Note:** The user interface is optimized for **desktop/laptop view only** and may not render properly on mobile devices.

<pre>
#### 🟢 Option 1: Use Deployed Versions (No Setup Needed)

- **Frontend (Chat UI):** [https://foodie-app.streamlit.app](https://foodie-app.streamlit.app)  
- **Backend API:** [https://foodie-backend-mq80.onrender.com](https://foodie-backend-mq80.onrender.com)

> **Instructions:**  
> First, click the **Backend API** link to wake up the Render server (it may take a few seconds).  
> Once it's running, click the **Frontend UI** link to launch the app and start chatting.

#### ⚙️ Option 2: Run Locally on Your Machine

**1. Clone the Repo**
 ```bash
    git clone https://github.com/Ola-doyin/Foodie-App.git
    cd Foodie-App
 ```

**2. Run the backend**
 ```bash
    cd foodie-backend
    pip install -r requirements.txt
    uvicorn components.backend:app --reload
 ```

**3. Run the frontend**
```bash
    cd foodie-frontend
    pip install -r requirements.txt
    streamlit run frontend.py
```

<div style="margin-top: 12px;"></div>

⚠️ **Make sure to add your Gemini API key in a .env.txt file in the foodie-frontend folder like this:**
```bash
    GEMINI_API_KEY=your_google_gemini_api_key_here
```
</pre>

<br>


## ⚙️ Features

- 🌐 Multilingual: Supports English, Yoruba, Hausa, Igbo, and Pidgin
- 🧠 Gemini-powered: ChatGPT-style natural responses
- 📷 Image Uploads: Send food pictures with queries
- 🍱 View menu by category
- 🧾 Order food (deducts from wallet)
- 🪑 Book tables at selected branches
- 📍 View all branches and their current specials
- 💬 Interactive chat bubbles with avatars


<br>


## 🏗️ Project Structure
```md
Foodie-App/
├── foodie-frontend/ # Streamlit app
│ ├── assets/ # Images, logo, background
│ ├── components/ # style.py, prompt.py, tools.py
│ ├── env.txt # Gemini API key (local only)
│ └── frontend.py # Main Streamlit entry
│
├── foodie-backend/ # FastAPI backend
│ ├── components/
│ │ └── backend.py # All backend endpoints
│ ├── foodie_database/
│ │ └── original_data.py # Initial dataset
│ ├── user.json # Runtime user data
│ ├── menu.json # Runtime menu
│ ├── branches.json # Runtime branch info
│ └── requirements.txt # Backend dependencies
```


<br>


## 🔧 Tech Stack

| Layer     | Technology                    |
|-----------|-------------------------------|
| Frontend  | Streamlit                     |
| Backend   | FastAPI, Pydantic             |
| AI Model  | Google Gemini Pro (via API)   |
| Hosting   | Render (backend), Streamlit Cloud (frontend) |
| Styling   | Pure CSS injected via Python  |
| Data Store| JSON (simulated DB)           |


<br>


## 💬 Sample Prompts Examples

- “Show me all soups on the menu”
- “Book a VIP table in Ikeja”
- “How much is Jollof Rice and Chicken Wings”
- “How much do I have in my wallet?”
- “What was my last order?”
- “You sabi semo abi?”
- “Ki ni mo le je?”
  

<br>


## 📄 License
MIT License © Oladoyin Arewa

Creator: Oladoyin Arewa

👩‍🔬 Electrical Engineer | 🧠 AI/ML Enthusiast | 🌞 Solar Microgrid Researcher

GitHub: [@Ola-doyin](https://github.com/Ola-doyin)  

<br>
<br>


### 💖 Built with love by Oladoyin
Have fun with the foodie chatbot!!!
