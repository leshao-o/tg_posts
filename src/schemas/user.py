from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    name: str
    email: EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserAdd(BaseModel):
    name: str
    email: EmailStr
    hashed_password: str


class User(UserAdd):
    id: int
