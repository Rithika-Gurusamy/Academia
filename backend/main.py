from fastapi import FastAPI, Depends, HTTPException, Query, Body
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import JSONB
from database import SessionLocal, engine
import models
import schemas
from typing import Optional, List
from models import User
from models import Student
from datetime import date
from auth import hash_password, verify_password
from fastapi.middleware.cors import CORSMiddleware
import random
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

# Email Configuration
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")


def send_email(subject, recipient, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Successfully sent email to {recipient}")
        return True
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to send email: {e}")
        return False

try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: create_all failed: {e}")

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://academia-five-dun.vercel.app",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://localhost:3000",
    ],
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

@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if user.role not in ["student", "faculty"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    existing_email = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    try:
        new_user = models.User(
            username=user.username,
            email=user.email,
            password_hash=hash_password(user.password),
            role=user.role
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "Account created"}
    except Exception as e:
        db.rollback()
        print(f"SIGNUP ERROR: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
class LoginRequest(BaseModel):
    username: str
    password: str
    role: str

@app.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username, User.role == data.role).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials or role")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    register_no = None
    if data.role == "student":
        student = db.query(models.Student).filter(models.Student.user_id == user.id).first()
        if student:
            register_no = student.register_no

    return {
        "message": "Login successful",
        "role": user.role,
        "user_id": user.id,
        "register_no": register_no
    }

@app.post("/student/profile")
def create_student_profile(user_id: int, student_in: schemas.StudentCreate, db: Session = Depends(get_db)):
    user_existing = db.query(models.Student).filter(models.Student.user_id == user_id).first()
    if user_existing:
        raise HTTPException(status_code=400, detail="You already have a profile.")

    # Check if student already exists by reg no
    existing = db.query(models.Student).filter(models.Student.register_no == student_in.register_no).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student with this register number already exists")

    try:
        new_student = models.Student(**student_in.model_dump())
        new_student.user_id = user_id
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return {"message": "Student profile created successfully", "student": new_student}
    except Exception as e:
        db.rollback()
        print(f"PROFILE CREATE ERROR: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/student/list")
def get_student_list(
    from_reg: Optional[str] = None,
    to_reg: Optional[str] = None,
    gender: Optional[str] = None,
    scholar_type: Optional[str] = None,
    community: Optional[str] = None,
    blood_group: Optional[str] = None,
    first_graduate: Optional[bool] = None,
    sc_st_scholarship: Optional[bool] = None,
    pudhumai_pen: Optional[bool] = None,
    mbc_bc_scholarship: Optional[bool] = None,
    pmss_scholarship: Optional[bool] = None,
    category_7_5_scholarship: Optional[bool] = None,
    mudhalvan_scholarship: Optional[bool] = None,
    other_scholarship: Optional[bool] = None,
    project_domain: Optional[List[str]] = Query(None),
    cert_domain: Optional[List[str]] = Query(None),
    has_projects: Optional[bool] = None,
    has_certifications: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Student)

    # Register Number Range
    if from_reg:
        query = query.filter(Student.register_no >= from_reg)
    if to_reg:
        query = query.filter(Student.register_no <= to_reg)

    # Direct Matches
    if gender:
        query = query.filter(Student.gender == gender)
    if scholar_type:
        query = query.filter(Student.scholar_type == scholar_type)

    # Case-Insensitive Matches
    if community:
        query = query.filter(Student.community.ilike(community))
    if blood_group:
        query = query.filter(Student.blood_group.ilike(blood_group))

    # Booleans (only apply if value is checked/provided as True)
    if first_graduate:
        query = query.filter(Student.first_graduate == True)
    if sc_st_scholarship:
        query = query.filter(Student.sc_st_scholarship == True)
    if pudhumai_pen:
        query = query.filter(Student.pudhumai_pen == True)
    if mbc_bc_scholarship:
        query = query.filter(Student.mbc_bc_scholarship == True)
    if pmss_scholarship:
        query = query.filter(Student.pmss_scholarship == True)
    if category_7_5_scholarship:
        query = query.filter(Student.category_7_5_scholarship == True)
    if mudhalvan_scholarship:
        query = query.filter(Student.mudhalvan_scholarship == True)
    if other_scholarship:
        query = query.filter(Student.other_scholarship == True)

    if has_projects or project_domain:
        sub_query = db.query(models.Project.student_id)
        if project_domain:
            # Match ANY of the selected domains (OR logic for flexibility)
            sub_query = sub_query.filter(or_(*[models.Project.domains.cast(JSONB).contains([d.lower()]) for d in project_domain]))
        query = query.filter(models.Student.id.in_(sub_query))
    
    if has_certifications or cert_domain:
        sub_query = db.query(models.Certification.student_id)
        if cert_domain:
            # Match ANY of the selected domains
            sub_query = sub_query.filter(or_(*[models.Certification.domains.cast(JSONB).contains([d.lower()]) for d in cert_domain]))
        query = query.filter(models.Student.id.in_(sub_query))

    return query.order_by(Student.register_no).all()

@app.get("/student/profile/{register_no}")
def get_student_profile(register_no: str, user_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    if user_id is not None:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user and user.role == "student":
            # Check if this user already has a DIFFERENT profile saved
            user_profile = db.query(models.Student).filter(models.Student.user_id == user_id).first()
            if user_profile and user_profile.register_no != register_no:
                raise HTTPException(status_code=403, detail="Restricted: You have already saved your data under your own register number.")

    student = db.query(Student).filter(Student.register_no == register_no).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if user_id is not None:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user and user.role == "student":
            if student.user_id is not None and student.user_id != user_id:
                raise HTTPException(status_code=403, detail="Restricted: You cannot view someone else's profile.")

    return student

@app.put("/student/profile/{register_no}")
def update_student_profile(
    register_no: str,
    student_update: schemas.StudentUpdate,
    user_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    student = db.query(models.Student).filter(models.Student.register_no == register_no).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if user_id is not None:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user and user.role == "student":
            if student.user_id is not None and student.user_id != user_id:
                raise HTTPException(status_code=403, detail="Restricted: You cannot update someone else's profile.")

    # Update only provided fields
    update_data = student_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)

    db.commit()
    db.refresh(student)

    return {"message": "Student profile updated successfully", "student": student}

# Recovery Features
class EmailRequest(BaseModel):
    email: str

class OTPRequest(BaseModel):
    email: str
    otp_code: str

class ResetPasswordRequest(BaseModel):
    email: str
    otp_code: str
    new_password: str

@app.post("/forgot-password")
def forgot_password(data: EmailRequest, db: Session = Depends(get_db)):
    email = data.email.strip()
    user = db.query(models.User).filter(models.User.email.ilike(email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    otp_code = str(random.randint(100000, 999999))
    expires_at = int(time.time()) + 300  # 5 minutes

    # Clean old OTPs for this email
    db.query(models.OTP).filter(models.OTP.email.ilike(email)).delete(synchronize_session=False)
    
    new_otp = models.OTP(email=email, otp_code=otp_code, expires_at=expires_at)
    db.add(new_otp)
    db.commit()

    if not send_email("Password Reset OTP", email, f"Your OTP for password reset is: {otp_code}. It expires in 5 minutes."):
        raise HTTPException(status_code=500, detail="Failed to send email. Check backend configuration.")
    return {"message": "OTP sent to email"}

@app.post("/forgot-username")
def forgot_username(data: EmailRequest, db: Session = Depends(get_db)):
    email = data.email.strip()
    user = db.query(models.User).filter(models.User.email.ilike(email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    otp_code = str(random.randint(100000, 999999))
    expires_at = int(time.time()) + 300  # 5 minutes

    db.query(models.OTP).filter(models.OTP.email.ilike(email)).delete(synchronize_session=False)
    
    new_otp = models.OTP(email=email, otp_code=otp_code, expires_at=expires_at)
    db.add(new_otp)
    db.commit()

    if not send_email("Username Recovery OTP", email, f"Your OTP for username recovery is: {otp_code}. It expires in 5 minutes."):
        raise HTTPException(status_code=500, detail="Failed to send email. Check backend configuration.")
    return {"message": "OTP sent to email"}

@app.post("/verify-otp")
def verify_otp(data: OTPRequest, db: Session = Depends(get_db)):
    email = data.email.strip()
    otp_code = data.otp_code.strip()
    otp_record = db.query(models.OTP).filter(models.OTP.email.ilike(email)).first()
    
    if not otp_record:
        raise HTTPException(status_code=400, detail="No OTP found for this email")

    if otp_record.attempts >= 3:
        db.delete(otp_record)
        db.commit()
        raise HTTPException(status_code=400, detail="Max attempts reached. Request a new OTP.")

    if otp_record.expires_at < int(time.time()):
        db.delete(otp_record)
        db.commit()
        raise HTTPException(status_code=400, detail="OTP expired")

    if otp_record.otp_code != otp_code:
        otp_record.attempts += 1
        db.commit()
        raise HTTPException(status_code=400, detail="Invalid OTP")

    return {"message": "OTP verified"}

@app.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    email = data.email.strip()
    otp_code = data.otp_code.strip()
    otp_record = db.query(models.OTP).filter(models.OTP.email.ilike(email), models.OTP.otp_code == otp_code).first()
    
    if not otp_record or otp_record.expires_at < int(time.time()):
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    user = db.query(models.User).filter(models.User.email.ilike(email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password_hash = hash_password(data.new_password)
    db.delete(otp_record)
    db.commit()

    return {"message": "Password reset successful"}

@app.post("/retrieve-username")
def retrieve_username(data: OTPRequest, db: Session = Depends(get_db)):
    email = data.email.strip()
    otp_code = data.otp_code.strip()
    otp_record = db.query(models.OTP).filter(models.OTP.email.ilike(email), models.OTP.otp_code == otp_code).first()
    
    if not otp_record or otp_record.expires_at < int(time.time()):
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    user = db.query(models.User).filter(models.User.email.ilike(email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    username = user.username
    # Mask username
    masked_username = username[0] + "*" * (len(username) - 2) + username[-1] if len(username) > 2 else username

    db.delete(otp_record)
    db.commit()

    return {"username": username, "masked_username": masked_username}

# Project & Certification Features
@app.post("/student/{register_no}/projects")
def add_project(register_no: str, project_in: schemas.ProjectCreate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.register_no == register_no).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    new_project = models.Project(
        student_id=student.id,
        description=project_in.description,
        domains=project_in.domains,
        github_link=project_in.github_link
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    # Log activity
    log = models.ActivityLog(
        student_id=student.id,
        activity_type="project_added",
        reference_id=new_project.id
    )
    db.add(log)
    db.commit()

    return new_project

@app.get("/student/{register_no}/projects")
def get_projects(register_no: str, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.register_no == register_no).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return db.query(models.Project).filter(models.Project.student_id == student.id).all()

@app.post("/student/{register_no}/certifications")
def add_certification(register_no: str, cert_in: schemas.CertificationCreate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.register_no == register_no).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    new_cert = models.Certification(
        student_id=student.id,
        description=cert_in.description,
        domains=cert_in.domains,
        certificate_link=cert_in.certificate_link
    )
    db.add(new_cert)
    db.commit()
    db.refresh(new_cert)

    # Log activity
    log = models.ActivityLog(
        student_id=student.id,
        activity_type="cert_added",
        reference_id=new_cert.id
    )
    db.add(log)
    db.commit()

    return new_cert

@app.get("/student/{register_no}/certifications")
def get_certifications(register_no: str, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.register_no == register_no).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return db.query(models.Certification).filter(models.Certification.student_id == student.id).all()

@app.get("/faculty/activity-logs")
def get_activity_logs(db: Session = Depends(get_db)):
    logs = db.query(
        models.ActivityLog, 
        models.Student.name.label("student_name"),
        models.Student.register_no.label("register_no")
    ).join(models.Student).filter(models.ActivityLog.seen_by_faculty == False).all()
    
    result = []
    for log, name, reg in logs:
        log_data = schemas.ActivityLog.from_orm(log)
        log_data.student_name = name
        log_data.register_no = reg
        
        # Populate details based on type
        if log.activity_type == "project_added":
            item = db.query(models.Project).filter(models.Project.id == log.reference_id).first()
            if item:
                log_data.description = item.description
                log_data.domains = item.domains
                log_data.link = item.github_link
        elif log.activity_type == "cert_added":
            item = db.query(models.Certification).filter(models.Certification.id == log.reference_id).first()
            if item:
                log_data.description = item.description
                log_data.domains = item.domains
                log_data.link = item.certificate_link
                
        result.append(log_data)
        
    return result

@app.post("/faculty/activity-logs/{log_id}/seen")
def mark_log_seen(log_id: int, db: Session = Depends(get_db)):
    log = db.query(models.ActivityLog).filter(models.ActivityLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    log.seen_by_faculty = True
    db.commit()
    return {"message": "Marked as seen"}

@app.delete("/student/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.query(models.ActivityLog).filter(models.ActivityLog.activity_type == "project_added", models.ActivityLog.reference_id == project_id).delete()
    db.delete(project)
    db.commit()
    return {"message": "Project deleted"}

@app.delete("/student/certifications/{cert_id}")
def delete_certification(cert_id: int, db: Session = Depends(get_db)):
    cert = db.query(models.Certification).filter(models.Certification.id == cert_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certification not found")
    db.query(models.ActivityLog).filter(models.ActivityLog.activity_type == "cert_added", models.ActivityLog.reference_id == cert_id).delete()
    db.delete(cert)
    db.commit()
    return {"message": "Certification deleted"}

