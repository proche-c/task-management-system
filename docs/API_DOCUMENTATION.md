# API Documentation

This document describes the core API endpoints of the Task Management System.

---

## Authentication

- **POST /api/auth/register/**  
  Register a new user.  
  **Body:** `{"username": "pepita", "password": "Password1234", "password2": "Password1234", "email": "pepita@example.com"}`

- **POST /api/auth/login/**  
  Obtain JWT token.  
  **Body:** `{"username": "john", "password": "Password1234"}`

- **POST /api/auth/logout/**  
  Invalidate the current token.

- **POST /api/auth/refresh/**  
  Refresh JWT token.

---

## Users

- **GET /api/users/**  
  List all users (with pagination).

- **GET /api/users/{id}/**  
  Get user details.

- **PUT /api/users/{id}/**  
  Update user information.

- **GET /api/users/me/**  
  Get the authenticated user's profile.

---

## Tasks

- **GET /api/tasks/**  
  List tasks (filtering, search, pagination supported).

- **POST /api/tasks/**  
  Create a new task.  
  **Body:** `{"title": "My Task", "description": "Details..."}`

- **GET /api/tasks/{id}/**  
  Retrieve task details.

- **PUT /api/tasks/{id}/**  
  Update task.

- **PATCH /api/tasks/{id}/**  
  Partial update of task.

- **DELETE /api/tasks/{id}/**  
  Delete a task.

### Task Operations

- **POST /api/tasks/{id}/assign/**  
  Assign users to a task.

- **POST /api/tasks/{id}/comments/**  
  Add a comment to a task.  


- **GET /api/tasks/{id}/comments/**  
  Retrieve comments of a task.

- **GET /api/tasks/{id}/history/**  
  Retrieve task history (audit log).

---

## Notes
- All endpoints except register and login require authentication (JWT).  
- Use the token in headers:  
  `Authorization: Bearer <your_token>`  

