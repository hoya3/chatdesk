from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ChatwootIdentity(BaseModel):
    identifier: str
    identifier_hash: str
    email: EmailStr
    name: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    chatwoot: ChatwootIdentity


class UserOut(BaseModel):
    id: str
    email: EmailStr
    name: str

    class Config:
        from_attributes = True


class MeResponse(BaseModel):
    user: UserOut
    chatwoot: ChatwootIdentity
