# Backend

A robust FastAPI backend powering real-time mock interviews with collaborative coding, slot scheduling, and JWT-based authentication.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | MongoDB |
| Real-time | WebSockets + WebRTC |
| Authentication | JWT (JSON Web Tokens) |
| Password Security | bcrypt |
| Validation | Pydantic |
| Server | Uvicorn |

---

## Project Structure

```
backend/
├── app/
│   ├── controllers/
│   │   ├── auth_controller.py
│   │   └── slot_controller.py
│   ├── routers/
│   │   ├── auth_router.py
│   │   ├── slot_router.py
│   │   └── user_router.py
│   ├── middleware/
│   │   └── auth_middleware.py
│   ├── schemas/
│   │   ├── user_schema.py
│   │   └── slot_schema.py
│   ├── websocket/
│   │   └── connection_manager.py
│   ├── utils/
│   │   ├── security.py
│   │   ├── jwt_handler.py
│   │   ├── serializer.py
│   │   ├── room_storage.py
│   │   └── cleanup_rooms.py
│   ├── database.py
│   └── main.py
└── rooms/
```

---

## Modules

### Module 1 — Authentication

Handles user registration, login, and route protection via JWT.

**Flow:**

```
Client Request → Router → Controller → Hash Password → Save to MongoDB → Issue JWT → Client
```

**Endpoints:**

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/signup` | Register a new user |
| `POST` | `/api/auth/login` | Login and receive JWT |
| `POST` | `/api/auth/logout` | Logout user |

**Key Files:**

- `schemas/user_schema.py` — Pydantic models for request validation
- `utils/security.py` — `hash_password()` and `verify_password()` using bcrypt
- `utils/jwt_handler.py` — JWT creation with `id` and `exp` payload
- `controllers/auth_controller.py` — Signup, login, logout logic
- `middleware/auth_middleware.py` — Validates `Authorization: Bearer <token>` on protected routes

---

### Module 2 — Interview Slot Scheduling

Manages creation, discovery, booking, and cancellation of interview slots.

**Slot Document Schema (MongoDB):**

```json
{
  "createdBy": "user_id",
  "startTime": "ISO Date",
  "endTime": "ISO Date",
  "duration": 60,
  "skills": ["Python", "System Design"],
  "isBooked": false,
  "bookedBy": null,
  "roomId": null
}
```

**Endpoints:**

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/slots/create` | Create a new interview slot |
| `POST` | `/api/slots/book/{slot_id}` | Book an available slot |
| `GET` | `/api/slots/available` | List all available slots |
| `GET` | `/api/slots/booked` | List user's booked slots |
| `DELETE` | `/api/slots/cancel/{slot_id}` | Cancel a slot |
| `GET` | `/api/slots/created-and-booked` | Slots created by and booked for the user |

**Booking Rules:**

- A user cannot book their own slot
- A slot must not already be booked
- A user cannot have overlapping slot times

**On successful booking**, the slot is updated:

```json
{
  "isBooked": true,
  "bookedBy": "candidate_id",
  "roomId": "uuid"
}
```

The `roomId` links directly to the live interview room.

---

### Module 3 — Real-Time Interview Room

Provides a live interview environment with collaborative code editing and WebRTC signaling over WebSockets.

**WebSocket Endpoint:**

```
/ws/{room_id}
```

**Supported Events:**

| Event | Purpose |
|---|---|
| `join-room` | User enters the interview room |
| `peer-connected` | Notify the other participant of a connection |
| `signal` | WebRTC signaling for peer-to-peer setup |
| `code-change` | Sync collaborative code editor state |

**Code Persistence:**

Editor state is saved to `rooms/{room_id}.txt`. On reconnection, an `initial-code` event restores the last known editor content.

**Room Cleanup:**

A background scheduler runs `cleanup_rooms()` every hour, removing rooms inactive for more than 5 hours to prevent file accumulation.

---

## Getting Started

### Prerequisites

- Python 3.9+
- MongoDB instance running locally or via Atlas

### Installation

```bash
pip install -r requirements.txt
```

### Running the Server

```bash
uvicorn app.main:app --reload
```

| Resource | URL |
|---|---|
| API Server | `http://127.0.0.1:8000` |
| Swagger Docs | `http://127.0.0.1:8000/docs` |

---

## Testing Guide

Recommended end-to-end test sequence using Swagger UI:

1. **Signup** — `POST /api/auth/signup`
2. **Login** — `POST /api/auth/login` → copy JWT token
3. **Authorize** — Click "Authorize" in Swagger and paste token
4. **Create Slot** — `POST /api/slots/create`
5. **View Available Slots** — `GET /api/slots/available`
6. **Book Slot** — `POST /api/slots/book/{slot_id}`
7. **Join Interview Room** — Connect via WebSocket at `/ws/{room_id}`

---

## End-to-End Flow

```
User A signs up
     ↓
User A creates an interview slot
     ↓
User B browses available slots
     ↓
User B books a slot
     ↓
Backend generates a unique roomId
     ↓
Both users connect to WebSocket room
     ↓
Live interview session begins (code editor + WebRTC)
```

---

## Future Improvements

- **Redis** — Scalable WebSocket pub/sub and room state storage
- **Docker** — Containerized deployment
- **Rate Limiting** — Protect public endpoints from abuse
- **Structured Logging** — Request tracing and error monitoring
- **Database Indexing** — Optimised MongoDB queries for slots and users

---

## Current Status

| Feature | Status |
|---|---|
| User Authentication | ✅ Complete |
| Interview Slot Scheduling | ✅ Complete |
| Slot Booking & Validation | ✅ Complete |
| Real-Time WebSocket Rooms | ✅ Complete |
| Collaborative Code Editor | ✅ Complete |
| Persistent Room State | ✅ Complete |
| Automatic Room Cleanup | ✅ Complete |

> Ready for frontend integration.
