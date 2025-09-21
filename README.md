# Candidate & Job Management System

A full-stack application built with **React (frontend)** and **FastAPI + MySQL (backend)**.  
The system allows **Admins** to manage jobs and candidates (add, update, delete), while **Candidates** can view and apply to jobs.  

It also includes **JWT-based authentication**, **role-based access control**, and **Swagger API documentation** for backend endpoints.

---

## 🚀 Features
- 🔑 User authentication (Admin / Candidate)
- 🧑‍💼 Candidate management (CRUD)
- 💼 Job postings management (CRUD)
- 📄 Resume upload (link input)
- 🔒 Role-based protected routes
- 📊 Swagger (OpenAPI) API documentation

---

## 🛠️ Technology Stack

### Backend (FastAPI + MySQL)
- [FastAPI](https://fastapi.tiangolo.com/) — Web framework
- [Uvicorn](https://www.uvicorn.org/) — ASGI server
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM
- [PyMySQL](https://pypi.org/project/PyMySQL/) — MySQL driver
- [Pydantic](https://docs.pydantic.dev/) — Data validation
- [python-dotenv](https://pypi.org/project/python-dotenv/) — Environment variables

### Frontend (React)
- [React](https://reactjs.org/)
- [React Router](https://reactrouter.com/) — Routing
- [Axios](https://axios-http.com/) — API requests
- [Tailwind CSS](https://tailwindcss.com/) — Styling

---

## ⚙️ Setup Instructions

### 🔹 Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Ravikanth1432/hr-project-3.git
   cd backend
Create a virtual environment:

bash
Copy code
py -m venv venv
source venv/Script/activate   # (Linux/Mac)
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Configure environment variables in .env:

env
Copy code
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/your_db_name
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
Run backend:

bash
Copy code
uvicorn main:app --reload
Open backend in browser:

API Root: http://localhost:8000

Swagger Docs: http://localhost:8000/docs

🔹 Frontend Setup
Go to frontend folder:

bash
Copy code
cd frontend
Install dependencies:

bash
Copy code
npm install
Start React dev server:

bash
Copy code
npm start
Open frontend in browser:

http://localhost:3000

📖 API Overview
🔐 Authentication
POST /login → User login (returns JWT token)

👤 Candidates
GET /candidates → List all candidates

POST /candidates → Add new candidate

PUT /candidates/{id} → Update candidate

DELETE /candidates/{id} → Delete candidate

💼 Jobs
GET /jobs → List all jobs

POST /jobs → Add new job

PUT /jobs/{id} → Update job

DELETE /jobs/{id} → Delete job



