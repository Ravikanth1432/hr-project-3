# backend/schemas.py
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    role: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    class Config:
        from_attributes = True

class CandidateBase(BaseModel):
    name: str
    email: str
    phone_number: str
    current_status: str
    resume_link: str

class CandidateCreate(CandidateBase): pass
class CandidateOut(CandidateBase):
    id: int
    class Config:
        from_attributes = True

class JobBase(BaseModel):
    title: str
    description: str
    required_skills: str
    recruiter_id: int

class JobCreate(JobBase): pass
class JobOut(JobBase):
    id: int
    class Config:
        from_attributes = True
