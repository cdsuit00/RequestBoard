RequestBoard

RequestBoard is a full-stack web application where users can sign up, log in, post requests, and respond to requests. It uses a Flask backend (with JWT authentication) and a React frontend to create a simple, modern workflow for managing requests.


Features

User Authentication (Signup, Login, Logout)
JWT-based Authorization for secure API access
Create, Read, Update, Delete (CRUD) requests
Add Responses to requests
Frontend Dashboard to view and manage requests
Protected Routes (only logged-in users can access the dashboard)

Tech Stack

Backend: Flask, Flask-Migrate, Flask-JWT-Extended, SQLAlchemy
Frontend: React, React Router, Axios
Database: SQLite (default, can swap to PostgreSQL/MySQL)

Installation & Setup
1. Clone the repository

git clone https://github.com/cdsuit00/requestboard.git
cd requestboard

2. Setup the backend (Flask)

cd backend
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Run server
flask run

Backend will be available at:
http://127.0.0.1:5000

3. Setup the frontend (React)

cd frontend
npm install
npm start

Frontend will be available at:
http://localhost:3000

API Endpoints
Authentication
  POST /signup → Create a new user
  POST /login → Login and receive JWT

Requests
  GET /requests → Get all requests (paginated)
  POST /requests → Create a request (auth required)
  PUT /requests/<id> → Update request (auth required, owner only)
  DELETE /requests/<id> → Delete request (auth required, owner only)

Responses
  POST /requests/<id>/responses → Add a response
  GET /requests/<id>/responses → Get responses for a request

Usage Flow

1. Sign up with a username, email, and password.
2. Log in to receive an access token.
3. Access the Dashboard to:
    Create requests
    View existing requests
    Respond to requests
    Edit or delete your own requests
4. Logout to clear the session.

