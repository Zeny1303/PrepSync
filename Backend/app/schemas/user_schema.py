'''
Step 1 :- User Schema (Request Validation)
'''

from pydantic import BaseModel, EmailStr
from typing import List

class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    skills: List[str]

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    skills: List[str]    