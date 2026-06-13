# ClearChat

A real-time communication backend built with FastAPI and WebSockets.

This project started as an exploration of WebSocket-based chat systems and gradually evolved into a backend-focused architecture project centered around authentication, protocol design, room management, and scalable real-time communication patterns.

The goal of this project was not to build a polished messaging platform UI, but to understand how modern real-time backend systems are structured internally.

---

# Features

## Authentication

* JWT-based authentication
* Password hashing using Argon2
* Token generation and validation
* Protected HTTP endpoints using FastAPI dependencies

## Real-Time Communication

* WebSocket-based messaging
* Event-driven message protocol
* Private messaging
* Room-based messaging
* Persistent room subscriptions

## Architecture

* Service-layer based backend structure
* Separation of concerns between:

  * API routes
  * WebSocket handlers
  * Services
  * Database models
* Protocol routing system for WebSocket events
* Structured connection manager

## Persistence

* SQLite-backed persistence (development)
* Persistent message history
* Room membership tracking
* User and room models

## Room System

* Public/private room support
* Membership-based room access
* HTTP-based room creation and joining
* WebSocket-based live room subscriptions

---

# Tech Stack

* Python
* FastAPI
* WebSockets
* SQLAlchemy
* SQLite
* JWT (python-jose)
* Passlib / Argon2

---

# Project Structure

```bash
app/
├── api/
│   ├── auth.py
│   ├── websocket.py
│   ├── room.py
│   └── deps.py
│
├── core/
│   └── security.py
│
├── db/
│   └── session.py
│
├── models/
│   ├── user.py
│   ├── message.py
│   ├── room.py
│   └── membership.py
│
├── services/
│   ├── message_service.py
│   ├── room_service.py
│   └── connection_manager.py
│
└── ws/
    ├── router.py
    └── handlers/
```

---

# WebSocket Protocol

The project uses an event-driven WebSocket protocol.

Example payload:

```json
{
  "type": "message",
  "payload": {
    "chat_type": "room",
    "room": "dev",
    "content": "hello"
  }
}
```

The backend routes events through dedicated handlers instead of relying on large conditional blocks.

---

# Current Status

This project is currently a backend-focused prototype and learning project.

The main focus areas explored were:

* WebSocket architecture
* Real-time communication systems
* Authentication and authorization
* Service-oriented backend design
* Persistent room and messaging systems

Frontend/UI development was intentionally kept minimal.

---

# Future Improvements

Potential future additions include:

* PostgreSQL migration
* Redis Pub/Sub integration
* Rate limiting
* Presence system (online/offline tracking)
* Read receipts and delivery states
* Audit logging
* RBAC/moderation system
* Docker deployment
* OAuth support

---

# Running Locally

## Clone the repository

```bash
git clone <repo_url>
cd clearchat
```

## Create virtual environment

```bash
python -m venv .venv
```

## Activate environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Create `.env`

```env
SECRET_KEY=your_secret_key
```

## Run the server

```bash
uvicorn main:app --reload
```

---

# Learning Notes

This project was built primarily as a systems/backend learning exercise focused on understanding:

* how real-time applications work internally
* WebSocket lifecycle management
* backend architecture patterns

The implementation intentionally prioritizes learning and experimentation over feature completeness.
