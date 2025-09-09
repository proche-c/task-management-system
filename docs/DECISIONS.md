# DECISIONS

This document outlines the main decisions taken during the project development.

---

## ✅ Completed Features and Why
- **JWT Authentication** (login, register, logout, refresh): core security feature and mandatory requirement.  
- **User Management**: endpoints for listing users, getting profile, and updating information.  
- **Task Management (CRUD)**: `Task` model fully implemented with relationships (`assigned_to`, `tags`, `parent_task`).  
- **Task Comments**: `Comment` model with associated endpoints.  
- **Task History**: endpoints to track changes in tasks.  
- **Celery Workers + Beat**: background tasks implemented:  
  - Email notifications.  
  - Daily summary.  AUN NO!!! 
  - Overdue task check. AUN NO!!!  
  - Cleanup of archived tasks. AUN NO!!! 
- **Docker Compose**: orchestrated services (Django, PostgreSQL, Redis, Celery, Celery Beat, Adminer).  
- **Basic Frontend with Django Templates**: task list, task detail, and simple forms.  

> Core mandatory features were prioritized to deliver a functional end-to-end system.

---

## ⏸️ Features Not Completed and Why. 
- **Password validation and SQL injection safeguards**: Due to time constraints, comprehensive validation for passwords and extra measures to prevent potential SQL injection attacks were not fully implemented. Django's ORM already provides strong protection against SQL injection, but additional validations (e.g., password complexity checks, input sanitization) could be added in a production environment.
- **Advanced UI**: kept a minimal frontend using templates instead of a full SPA.  
- **Team Management (`Team`) and Task Templates (`TaskTemplate`)**: out of scope due to time constraints.  
- **Real email notifications (SMTP)**: development uses `console.EmailBackend`.  
- **Full-text search in PostgreSQL**: only basic search with Django filters implemented.  

> These were skipped due to **time constraints** and because they were not critical for the demo.

---

## ⏳ Time Allocation
- **Docker infrastructure and initial setup**: 25%  
- **Modeling and REST API endpoints**: 35%  
- **Celery + Redis integration**: 20%  
- **Frontend with templates**: 10%  
- **Testing and adjustments**: 10%  

---

## ⚡ Technical Challenges
- **Integrating Celery + Redis in Docker**: configuring broker and workers to communicate correctly.  
- **JWT management with Django + DRF**: ensuring proper authentication and cookie handling in API calls.  
- **Complex relationships in `Task` model** (`assigned_to`, `tags`, `parent_task`) and their serialization.  
- **Auto-migrations in PostgreSQL within Docker container**.  

---

## ⚖️ Trade-offs
- **SSR with Django Templates vs. Modern SPA**: chose templates for simplicity and speed.  
- **Console email backend instead of real SMTP**: simplifies development and demo without external service setup.  
- **Partial feature implementation**: prioritized core feature quality over quantity.  

---

## 🚀 What Would Be Added With More Time 
- Password validation
- Real email notifications and optional WebSocket notifications.  
- Team management and task templates.  
- Advanced search with PostgreSQL `FullTextSearch`.  
- Comprehensive unit and integration tests.  

---

## 📌 Justification: Using Django Templates for Frontend
Django Templates were chosen because:  
1. The project requires only a **basic frontend for demonstration purposes**.  
2. Faster development within the same Django server.  
3. Avoids complexity of setting up a separate frontend service in Docker.  
4. Meets the minimum requirements to render tasks, details, and forms.  

---
