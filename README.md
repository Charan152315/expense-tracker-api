# 💰 Expense Tracker API - FastAPI + PostgreSQL + Docker

This is a fully functional backend Expense Tracker API built using **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **JWT Authentication**. The project is production-ready, containerized with **Docker**, and includes environment-based configurations for seamless deployment.

---

## 🚀 Features

- 🔐 JWT Authentication (Login & Register)
- 📊 Expense CRUD operations
- 📈 Monthly summary with total expenses
- 👥 Group creation and group-based expense tracking
- 🛠️ Dockerized setup for development and production
- 📦 PostgreSQL as the database
- 📁 Modular code structure (routes, schemas, models, utils)
- ✅ Tested using Postman and Pytest

---

## 🖼️ Project Architecture

app/
├── main.py
├── models/
├── routes/
├── schemas/
├── database.py
├── auth.py
├── config.py
├── utils.py
.env.prod
Dockerfile
docker-compose-prod.yml
init/init.sql

---

## ⚙️ Technologies Used

- [FastAPI](w)
- [PostgreSQL](w)
- [SQLAlchemy](w)
- [Alembic](w)
- [Docker](w)
- [Pytest](w)
- [Render](w) (for deployment)
- [pgAdmin](w)

---

## 🧪 API Endpoints (Examples)

### ✅ Register a user
`POST /users/`
```json
{
  "email": "charan@example.com",
  "password": "test1234",
  "monthly_limit": 5000
}
🔐 Login
POST /login

{
  "email": "charan@example.com",
  "password": "test1234"
}
💸 Create Expense
POST /expenses/

{
  "title": "Groceries",
  "amount": 1200,
  "description": "Bought vegetables",
  "category": "Food"
}
📊 View Summary
GET /summary/ (Requires JWT token)

🐳 Docker Setup (Production)

# Build and run containers
docker-compose -f docker-compose-prod.yml up --build

# Stop and remove containers
docker-compose -f docker-compose-prod.yml down -v
🛠️ Deployment (Render)
Live Link: Coming soon ✅

Connected with PostgreSQL + GitHub

Environment variables securely set

📄 .env.prod Format
env
Copy code
DATABASE_HOSTNAME=postgres
DATABASE_PORT=5432
DATABASE_NAME=fastapi
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=your_db_password
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

✍️ Author
Charan Sri

Student @ NIT Raipur, aspiring Backend + DevOps Engineer

LinkedIn

GitHub

⭐️ Show Some Love
If you liked this project, please ⭐️ the repo and share with your friends!

---









