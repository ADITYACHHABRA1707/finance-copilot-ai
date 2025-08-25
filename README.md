# Finance Copilot AI

Finance Copilot AI is a personal finance management and forecasting app built with **Streamlit (Frontend)**, **FastAPI (Backend)**, and integrated with **Portia AI** for intelligent decision-making and **Twilio WhatsApp API** for alerts.

---

##  Features

* **Expense Tracking**: Input and manage your daily expenses.
* **Forecasting**: Predict future trends using Portia AI or Prophet.
* **WhatsApp Alerts**: Get financial alerts directly on WhatsApp.
* **AI Simulation Mode**: Test without real Portia credentials.
* **Backend-Frontend Integration**: Streamlit UI communicates with FastAPI backend.

---

## 🛠 Tech Stack

* **Frontend**: Streamlit
* **Backend**: FastAPI + Uvicorn
* **Database**: SQLite (optional)
* **AI**: Portia AI API
* **Notifications**: Twilio WhatsApp API

---

## 📂 Project Structure

```
finance-copilot-ai/
├── app/               # Streamlit Frontend
│   ├── Home.py
│   └── pages/
│       ├── 1_Overview.py
│       ├── 2_Expenses.py
│       ├── 3_Forecast.py
├── backend/           # FastAPI Backend
│   ├── main.py
│   ├── services/
│       ├── portia_service.py
│       ├── whatsapp_alerts.py
├── .env               # Environment variables
├── requirements.txt
```

---

## ⚙️ Setup Instructions

### 1. Clone Repo

```bash
git clone https://github.com/yourusername/finance-copilot-ai.git
cd finance-copilot-ai
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure `.env`

Create a `.env` file in the root:

```
# Backend/DB
DB_URL=sqlite:///backend/data/finance.db

# Portia
PORTIA_BASE_URL=https://api.portia.ai/v1
PORTIA_API_KEY=your_portia_api_key
PORTIA_SIMULATE=true

# Twilio WhatsApp
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
USER_WHATSAPP_NUMBER=whatsapp:+91xxxxxxxxxx

# Frontend
BACKEND_URL=http://localhost:8000
```

### 5. Run Backend (FastAPI)

```bash
cd backend
uvicorn main:app --reload
```

### 6. Run Frontend (Streamlit)

```bash
cd app
streamlit run Home.py
```

---

##  Deployment Notes

* Update `BACKEND_URL` in `.env` when deploying backend.
* Switch `PORTIA_SIMULATE=false` when using real API keys.

---

##  Next Steps

* Add Portia AI integration for forecasting.
* Enable WhatsApp alerts via Twilio.
* Deploy on **Render/Railway** or **AWS**.

---

### Author: Aditya Chhabra
