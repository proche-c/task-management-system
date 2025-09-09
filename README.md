## Task Management System  

# Overview  

This project is a containerized Enterprise Task Management System built with Django, Django REST Framework, PostgreSQL, Redis, and Celery.  
It provides a REST API for authentication, user management, and task management, along with a simple frontend using Django templates.  
The project runs entirely in Docker and can be started with a single command.  

# Quick Start  

```bash
# Clone the repository
git clone <repo>
cd task-management-system

# Copy environment variables
cp .env.sample .env

# Start the application
docker-compose up
```

The following services will be started:  
+ PostgreSQL 15+ database
+ Redis 7+ for caching and Celery broker
+ Django application server (available at [http://localhost:8000](http://localhost:8000))
+ Celery worker for background tasks
+ Celery beat for scheduled tasks
+ adminer for DDBB visualization in the browser (available at [http://localhost:8080](http://localhost:8080))

