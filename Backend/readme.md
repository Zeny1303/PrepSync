
# Backend Architecture Overview


           main.py  (root)
              │
      ┌───────┼────────┐
   routers  controllers  database
      │           │          │
   auth.py     auth.py    mongodb
   slot.py     slot.py


The backend is implemented using FastAPI and follows a modular architecture where responsibilities are separated into routers, controllers, utilities, middleware, and database layers.

Initial backend structure:

Backend Tree

           main.py  (root)
              │
      ┌───────┼────────┐
   routers  controllers  database
      │           │          │
   auth.py     auth.py    mongodb
   slot.py     slot.py
Responsibility of each layer
Layer	Responsibility
main.py	Entry point of the backend server
routers	Define API endpoints
controllers	Business logic for each feature
database	MongoDB connection and collections
schemas	Request validation models
utils	Reusable utilities (JWT, hashing)
middleware	Authentication and request interception   

Module 1: Authentication System

The first module implemented in the backend is the Authentication System, which allows users to register, login, and access protected routes using JWT-based authentication.

Authentication flow:

Client Request
      ↓
Router (API endpoint)
      ↓
Controller (business logic)
      ↓
Database
      ↓
JWT Token Generated
      ↓
Client stores token
      ↓
Token sent with protected requests
      ↓
Authentication Middleware verifies token
Authentication Module Structure
Authentication Module
│
├── Step 1 → Request Schemas (user_schema.py)
├── Step 2 → Password Security
├── Step 3 → JWT Token Creation
├── Step 4 → Auth Controller (signup/login)
├── Step 5 → Auth Router (API endpoints)
└── Step 6 → Authentication Middleware
Step 1: Request Schemas

File:

app/schemas/user_schema.py

Pydantic schemas validate incoming request data before it reaches the controller.

Example schema:

class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    skills: List[str]

class UserLogin(BaseModel):
    email: EmailStr
    password: str

Purpose:

Validate request payload

Enforce required fields

Ensure correct data types

Equivalent concept in Node.js was handled by Mongoose schema validation.

Step 2: Password Security

File:

app/utils/security.py

Passwords are never stored in plain text. They are hashed using bcrypt.

Functions implemented:

hash_password()
verify_password()

Example:

hashed_password = hash_password(user.password)

Database stores:

$2b$12$2txldC93ItvHz.uiWtv5pu...

Benefits:

Protects user credentials

Prevents password leaks in case of database compromise

Uses salted hashing

Step 3: JWT Token Creation

File:

app/utils/jwt_handler.py

JWT (JSON Web Token) is used for stateless authentication.

When a user logs in successfully:

JWT Token = create_access_token(user_id)

Token payload contains:

{
  id: user_id,
  exp: expiration_time
}

Token example:

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Benefits:

Stateless authentication

No server-side sessions required

Scalable architecture

Step 4: Auth Controller

File:

app/controllers/auth_controller.py

The controller contains business logic for authentication.

Signup Logic
Check if user exists
      ↓
Hash password
      ↓
Store user in MongoDB
      ↓
Generate JWT token
      ↓
Return token + user
Login Logic
Find user by email
      ↓
Verify password
      ↓
Generate JWT token
      ↓
Return token

Logout simply removes the token on the client side.

Step 5: Auth Router

File:

app/routers/auth_router.py

Routers map API endpoints to controller functions.

Available endpoints:

Method	Endpoint	Description
POST	/api/auth/signup	Register new user
POST	/api/auth/login	Authenticate user
POST	/api/auth/logout	Logout user

Example router:

@router.post("/signup")
async def signup(user: UserSignup):
    return await auth_controller.signup(user)
Step 6: Authentication Middleware

File:

app/middleware/auth_middleware.py

Middleware verifies JWT tokens before allowing access to protected routes.

Flow:

Request received
      ↓
Extract Authorization header
      ↓
Decode JWT token
      ↓
Fetch user from database
      ↓
Attach user to request

Example protected route:

GET /api/user/me

Header required:

Authorization: Bearer TOKEN
Authentication Flow Summary
Signup
   ↓
User stored in MongoDB
   ↓
Login
   ↓
Password verification
   ↓
JWT token issued
   ↓
Token stored on client
   ↓
Client sends token in requests
   ↓
Middleware validates token
   ↓
Protected routes accessible
API Testing

Authentication APIs can be tested using:

FastAPI Swagger Docs

http://127.0.0.1:8000/docs

Thunder Client (VSCode)

Postman

Recommended testing sequence:

1️⃣ /api/auth/signup
2️⃣ /api/auth/login
3️⃣ /api/user/me (protected route)

Security Features Implemented

The authentication module includes:

Password hashing with bcrypt

JWT-based stateless authentication

Request validation with Pydantic

Protected routes using middleware

Secure user data handling