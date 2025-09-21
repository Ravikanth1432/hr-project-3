# backend/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
import models, schemas, auth
from database import SessionLocal, engine
from jose import JWTError, jwt

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ----------------------
# CORS Setup (important for frontend -> backend calls)
# ----------------------
origins = [
    "http://localhost:3000",  # React dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------
# Helper: Get current user from JWT
# ----------------------
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# ----------------------
# Auth Endpoints
# ----------------------
@app.post("/api/register", response_model=schemas.UserOut)
def register_user(
    user: schemas.UserCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "Admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    hashed_pw = auth.hash_password(user.password)
    db_user = models.User(email=user.email, password_hash=hashed_pw, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# ----------------------
# Candidate Endpoints
# ----------------------
@app.post("/api/candidates", response_model=schemas.CandidateOut)
def create_candidate(
    candidate: schemas.CandidateCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role not in ["Admin", "Recruiter"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_candidate = models.Candidate(**candidate.dict())
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

@app.get("/api/candidates", response_model=list[schemas.CandidateOut])
def get_candidates(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Candidate).all()

@app.get("/api/candidates/{candidate_id}", response_model=schemas.CandidateOut)
def get_candidate(candidate_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    cand = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    if not cand:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return cand

@app.put("/api/candidates/{candidate_id}", response_model=schemas.CandidateOut)
def update_candidate(candidate_id: int, candidate: schemas.CandidateCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role not in ["Admin", "Recruiter"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_candidate = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    if not db_candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    for key, value in candidate.dict().items():
        setattr(db_candidate, key, value)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

@app.delete("/api/candidates/{candidate_id}")
def delete_candidate(candidate_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != "Admin":
        raise HTTPException(status_code=403, detail="Only Admin can delete candidates")
    db_candidate = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    if not db_candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    db.delete(db_candidate)
    db.commit()
    return {"detail": "Candidate deleted"}

# ----------------------
# Job Endpoints
# ----------------------
@app.post("/api/jobs", response_model=schemas.JobOut)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role not in ["Admin", "Recruiter"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_job = models.Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@app.get("/api/jobs", response_model=list[schemas.JobOut])
def get_jobs(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Job).all()

@app.get("/api/jobs/{job_id}", response_model=schemas.JobOut)
def get_job(job_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.put("/api/jobs/{job_id}", response_model=schemas.JobOut)
def update_job(job_id: int, job: schemas.JobCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role not in ["Admin", "Recruiter"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    for key, value in job.dict().items():
        setattr(db_job, key, value)
    db.commit()
    db.refresh(db_job)
    return db_job

@app.delete("/api/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != "Admin":
        raise HTTPException(status_code=403, detail="Only Admin can delete jobs")
    db_job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(db_job)
    db.commit()
    return {"detail": "Job deleted"}

# ----------------------
# Application Endpoint
# ----------------------
@app.post("/api/jobs/{job_id}/apply")
def apply_for_job(job_id: int, candidate_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role not in ["Admin", "Recruiter", "HiringManager"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    db_application = models.Application(candidate_id=candidate_id, job_id=job_id)
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return {"detail": "Application submitted"}

# ----------------------
# Debug endpoint
# ----------------------
@app.get("/debug/users")
def debug_users(db: Session = Depends(get_db)):
    rows = db.query(models.User).all()
    return [{"id": u.id, "email": u.email, "role": u.role} for u in rows]
