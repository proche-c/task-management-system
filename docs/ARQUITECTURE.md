# Architecture

## Overview
The Task Management System is a full-stack application built with **Django** as the backend framework and **Django templates** as the frontend rendering engine.  
The system is fully containerized using **Docker Compose**, orchestrating multiple services that work together to provide authentication, task management, and background processing.

---

## Components

### 1. Django Application Server
- Provides the REST API (built with Django REST Framework).
- Serves the basic frontend pages using Django templates.
- Handles authentication, user management, and task management.
- Exposes endpoints on **http://localhost:8000**.

### 2. PostgreSQL Database
- Stores all persistent data: users, tasks, comments, tags, etc.
- Uses Django ORM with proper relations, constraints, and indexing.
- Data is persisted in Docker volumes to survive restarts.

### 3. Redis
- Used as the **Celery broker** and cache backend.
- Enables asynchronous background processing.

### 4. Celery Workers
- Process background jobs such as:
  - Sending task notifications.
  - Generating daily summaries. 
  - Checking overdue tasks. 
  - Cleaning up archived tasks. 


### 5. Celery Beat
- Scheduler that periodically triggers background jobs:
  - Daily summaries. 
  - Hourly overdue checks. 
  - Weekly cleanup of archived tasks. 

### 6. Adminer
- Simple web-based database client.
- Provides an interface to inspect and debug the PostgreSQL database in the browser.

---

## Inter-Service Communication
- Django communicates with **PostgreSQL** via the Django ORM.  
- Django pushes background tasks to **Redis**, which are picked up by Celery workers.  
- Celery Beat also schedules tasks into Redis, consumed by the workers.  
- Adminer connects directly to PostgreSQL for database inspection.

---

## Docker Setup
The application runs with a single command:

```bash
docker-compose up
```
