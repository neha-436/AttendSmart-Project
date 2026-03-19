from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from . import models, schemas
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "AttendSmart API running"}


@app.post("/users")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user:
        return {"error": "User not found"}

    if db_user.password != user.password:
        return {"error": "Incorrect password"}

    return {
        "message": "Login successful",
        "user_id": db_user.id,
        "name": db_user.name
    }

@app.post("/timetable")
def create_timetable(entry: schemas.TimetableCreate, db: Session = Depends(get_db)):

    new_entry = models.Timetable(
        user_id=entry.user_id,
        day=entry.day,
        subject=entry.subject,
        start_time=entry.start_time,
        end_time=entry.end_time
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry

@app.get("/timetable/{user_id}")
def get_timetable(user_id: int, db: Session = Depends(get_db)):
    timetable = db.query(models.Timetable).filter(models.Timetable.user_id == user_id).all()
    return timetable

@app.get("/subjects")
def get_subjects(db: Session = Depends(get_db)):
    subjects = db.query(models.Subject).all()
    return subjects

@app.post("/attendance")
def mark_attendance(entry: schemas.AttendanceCreate, db: Session = Depends(get_db)):

    new_record = models.Attendance(
        user_id=entry.user_id,
        subject=entry.subject,
        date=entry.date,
        status=entry.status
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record

@app.get("/attendance/{user_id}")
def get_attendance_stats(user_id: int, db: Session = Depends(get_db)):

    records = db.query(models.Attendance).filter(models.Attendance.user_id == user_id).all()

    stats = {}

    for r in records:
        subject = r.subject

        if subject not in stats:
            stats[subject] = {"total": 0, "present": 0}

        stats[subject]["total"] += 1

        if r.status == "present":
            stats[subject]["present"] += 1

    result = []

    for subject, data in stats.items():
        percentage = (data["present"] / data["total"]) * 100

        result.append({
            "subject": subject,
            "total_classes": data["total"],
            "attended": data["present"],
            "attendance_percentage": round(percentage, 2)
        })

    return result

@app.get("/safe_skip/{user_id}")
def safe_skip(user_id: int, db: Session = Depends(get_db)):

    records = db.query(models.Attendance).filter(models.Attendance.user_id == user_id).all()

    stats = {}

    for r in records:
        subject = r.subject

        if subject not in stats:
            stats[subject] = {"total": 0, "present": 0}

        stats[subject]["total"] += 1

        if r.status == "present":
            stats[subject]["present"] += 1

    result = []

    for subject, data in stats.items():
        total = data["total"]
        present = data["present"]

        attendance = (present / total) * 100

        min_required = 0.75

        max_skips = present - (min_required * total)

        result.append({
            "subject": subject,
            "attendance_percentage": round(attendance, 2),
            "safe_skips_remaining": max(0, int(max_skips))
        })

    return result