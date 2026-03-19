from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class TimetableCreate(BaseModel):
    user_id: int
    day: str
    subject: str
    start_time: str
    end_time: str

class AttendanceCreate(BaseModel):
    user_id: int
    subject: str
    date: str
    status: str