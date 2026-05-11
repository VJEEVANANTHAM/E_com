# E-Commerce Platform (E_com)

A modern full-stack e-commerce application built with a FastAPI backend and a Vite + React frontend.

## 🚀 Features
* Backend: FastAPI, SQLAlchemy (ORM), Pydantic schemas.
* Frontend: React.js, Vite, Tailwind CSS.
* Database: SQLite/PostgreSQL support.
* Architecture: Modular structure with separate routes, models, and schemas.

---

## 🛠️ Project Structure
E_com/
├── Backend/          # FastAPI Source Code
│   ├── curd/         # CRUD operations
│   ├── models/       # SQLAlchemy database models
│   ├── routes/       # API endpoints
│   ├── schemas/      # Pydantic data validation
│   ├── database.py   # DB connection config
│   └── main.py       # Entry point
├── Frontend/         # React + Vite Source Code
│   ├── src/          # Components and logic
│   └── public/       # Static assets
└── .gitignore        # Files to ignore

---

## ⚙️ Setup Instructions

### 1. Backend Setup (FastAPI)
Navigate to the backend directory and set up a virtual environment:
1. cd Backend
2. python -m venv .venv
3. Activation:
   - Windows: .\venv\Scripts\activate
   - Mac/Linux: source .venv/bin/activate
4. pip install -r requirements.txt

Run the server:
uvicorn main:app --reload

---

### 2. Frontend Setup (React + Vite)
1. cd Frontend
2. npm install
3. npm run dev

---

