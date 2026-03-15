# Rentify

Rentify is a full-stack web application for searching and managing rental properties.

The project is built as a learning and portfolio project to demonstrate full-stack development with Django and Next.js.

---

## Tech Stack

### Backend
- Django
- Django REST Framework
- MySQL
- JWT Authentication

### Frontend
- Next.js
- React
- TypeScript
- TailwindCSS
- React Query
- Axios

---

## Features (planned)

- User authentication (JWT)
- Property listings
- Property filters and pagination
- Property details page
- Booking requests
- Reviews and ratings
- Favorites
- Image uploads

---

## Project Structure

rentify/
│
├── backend/
│   └── Django REST API
│
├── frontend/
│   └── Next.js application
│
└── README.md

---

## API (draft)

### Auth

POST   /api/auth/register  
POST   /api/auth/login  
POST   /api/auth/refresh  
GET    /api/users/me  

### Properties

GET    /api/properties  
GET    /api/properties/:id  
POST   /api/properties  
PATCH  /api/properties/:id  
DELETE /api/properties/:id  

### Bookings

POST   /api/bookings  
GET    /api/bookings  
PATCH  /api/bookings/:id  

### Reviews

POST   /api/properties/:id/reviews  
GET    /api/properties/:id/reviews  

---

## Development Setup

### Backend

cd backend  
python -m venv .venv  
source .venv/bin/activate  
pip install -r requirements.txt  
python manage.py runserver  

### Frontend

cd frontend  
npm install  
npm run dev  

Frontend runs on:  
http://localhost:3000  

Backend API runs on:  
http://localhost:8000  

---

## Status

Work in progress.

This project is currently under active development.