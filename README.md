# 💰 Expense Tracker API - FastAPI + PostgreSQL + Docker

This is a fully functional backend **Expense Tracker API** built using **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **JWT Authentication**. The project is production-ready, containerized with **Docker**, tested using **Pytest**, and deployed on both **Render** and **AWS EC2**.

---

## 🚀 Features

- 🔐 JWT Authentication (Login & Register)
- 📊 Expense CRUD operations
- 📈 Monthly summary with total expenses
- 👥 Group creation and group-based expense tracking
- 🛠️ Dockerized setup for development and production
- 📦 PostgreSQL as the database
- 🧪 Tested using Pytest and Postman
- ☁️ Live deployment on AWS EC2 and Render
- 🔐 Environment-based secure configuration

---

## 🖼️ Project Architecture

app/
├── main.py
├── models.py
├── routes/
├── schemas.py
├── database.py
├── auth.py
├── config.py
├── utils.py
.env.prod
Dockerfile
docker-compose-prod.yml
docker-compose-dev.yml
init/init.sql



---

## ⚙️ Technologies Used

- [FastAPI](w)
- [PostgreSQL](w)
- [SQLAlchemy](w)
- [Alembic](w)
- [Docker](w)
- [Pytest](w)
- [Render](w) – Deployment
- [AWS EC2](w) + [S3](w) – Deployment
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

json
Copy
Edit
{
  "email": "charan@example.com",
  "password": "test1234"
}
💸 Create Expense
POST /expenses/

json
Copy
Edit
{
  "title": "Groceries",
  "amount": 1200,
  "description": "Bought vegetables",
  "category": "Food"
}
📊 View Summary
GET /summary/ (Requires JWT Token)

🐳 Docker Setup (Production)
Build and run containers
bash
Copy
Edit
docker-compose -f docker-compose-prod.yml up --build
Stop and remove containers
bash
Copy
Edit
docker-compose -f docker-compose-prod.yml down -v
📄 .env.prod Format
env
Copy
Edit
DATABASE_HOSTNAME=postgres
DATABASE_PORT=5432
DATABASE_NAME=your_db_name
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=your_db_password
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
TEST_DATABASE_NAME=your_test_db_name


☁️ Deployment
✅ Render: https://expense-tracker-api-ksno.onrender.com

✅ AWS EC2: http://13.61.195.207

🔗 Useful Links
📂 GitHub Repository: expense-tracker-api (https://github.com/Charan152315/expense-tracker-api.git)

💼 LinkedIn: Charansri Chintamaneni (https://www.linkedin.com/in/Charansri-chintamaneni))

✍️ Author
Charan Sri
Student @ NIT Raipur
Aspiring Backend + DevOps Engineer

⭐ Show Some Love
If you found this project helpful, please ⭐ the repo and share it with others!


---









