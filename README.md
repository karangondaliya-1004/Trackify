# Trackify – SaaS Authentication & Authorization Service

Trackify is a backend service built using **FastAPI** that provides secure, scalable, and production-ready **authentication and authorization** capabilities for modern applications.

It is designed to act as a **core identity service** that can power web applications, mobile apps, and microservices by handling user authentication, token management, and protected access in a standardized way.

This project emphasizes **clean architecture, security best practices, and real-world backend engineering patterns**.

---

## Project Overview

Trackify focuses on solving a fundamental problem faced by almost every software product:

> *How do we securely identify users and control access to APIs?*

The service offers:
- User identity management
- Secure login flows
- Token-based authentication
- Authorization enforcement for protected resources
- Health and readiness checks for deployments

It is intentionally built as a **backend-only service** so it can be reused across multiple frontends or integrated into larger systems.

---

## Scope of the Project

Trackify currently supports:

- Email & password based authentication
- JWT access and refresh token strategy
- Secure password storage
- Protected API endpoints
- Database-backed persistence
- Environment-based configuration
- Database health monitoring

The system is structured so that new features (roles, permissions, OAuth, etc.) can be added without rewriting existing logic.

---

## Core Functionalities

### Authentication
- User registration with validation
- Secure password hashing
- User login with credential verification

### Authorization
- JWT-based access control
- Bearer token authentication
- Dependency-based route protection

### Token Management
- Short-lived access tokens
- Long-lived refresh tokens
- Token expiration handling
- Invalid token protection

### Health Monitoring
- Application health endpoint
- Database connectivity verification

---

## Authentication Flow (High-Level)

1. A user registers using an email and password
2. The password is hashed and stored securely
3. The user logs in with valid credentials
4. The server issues:
   - An **access token** (short-lived)
   - A **refresh token** (long-lived)
5. The access token is sent with protected API requests
6. Tokens are validated on every request
7. Expired or invalid tokens are rejected safely

---

## How to Run the Project

### 1️Clone the repository

```bash
git clone <repository-url>
cd trackify
```

---

### 2️Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

---

### Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4Configure environment variables

Create a `.env` file in the project root:

```env
APP_NAME=Trackify
ENVIRONMENT=development

DATABASE_URL=sqlite:///./trackify.db

SECRET_KEY=your-super-secret-key
ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

#### Environment Variable Explanation

- `DATABASE_URL` – Database connection string
- `SECRET_KEY` – Used to sign JWT tokens (must be kept secret)
- `ALGORITHM` – JWT signing algorithm
- `ACCESS_TOKEN_EXPIRE_MINUTES` – Access token lifetime
- `REFRESH_TOKEN_EXPIRE_DAYS` – Refresh token lifetime

---

## Running the Application

```bash
uvicorn app.main:app --reload
```

The server will be available at:

```
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI provides interactive API documentation:

- Swagger UI  
  👉 http://127.0.0.1:8000/docs

From here you can:
- Register users
- Authenticate users
- Obtain tokens
- Call protected endpoints

---

## Security Considerations

- Passwords are never stored in plain text
- JWTs are cryptographically signed
- Tokens are validated on every request
- Expired and malformed tokens are rejected
- Secrets are loaded from environment variables
- Database sessions are safely opened and closed

---

## Future Enhancements

- Role-based access control (RBAC)
- OAuth (Google, GitHub, etc.)
- Email verification
- Password reset workflows
- Token revocation & blacklisting
- Rate limiting and monitoring