from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, DateTime, JSON, func
from sqlalchemy.dialects.postgresql import JSONB
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)

class OTP(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    otp_code = Column(String(6), nullable=False)
    expires_at = Column(Integer, nullable=False)  # Unix timestamp
    attempts = Column(Integer, default=0)


class Student(Base): 
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    # 1) General Information
    name = Column(String, nullable=False)
    register_no = Column(String, unique=True, nullable=False)
    roll_no = Column(String)
    mobile_no = Column(String)
    date_of_birth = Column(Date)
    gender = Column(String)
    scholar_type = Column(String) # Day Scholar / Hosteller
    blood_group = Column(String)
    email_personal = Column(String)
    email_college = Column(String)
    residential_address = Column(String)
    nationality = Column(String)
    community = Column(String)
    caste = Column(String)
    religion = Column(String)
    father_name = Column(String)
    father_mobile_no = Column(String)
    father_occupation = Column(String)
    mother_name = Column(String)
    mother_mobile_no = Column(String)
    mother_occupation = Column(String)
    guardian_name = Column(String)
    guardian_mobile_no = Column(String)
    guardian_occupation = Column(String)
    family_annual_income = Column(String)
    is_special_admission = Column(String) # yes / no
    is_differently_abled = Column(String) # yes / no

    # 2) Academic Info
    umis_number = Column(String)
    emis_number = Column(String)
    academic_year_of_joining = Column(String)
    course_type = Column(String) # ug / pg
    branch_specialization = Column(String)
    mode_of_study = Column(String) # lateral / regular
    type_of_admission = Column(String) # gq / mq
    medium_of_instruction = Column(String)
    date_of_admission = Column(Date)
    counselling_admission_number = Column(String)

    # 3) Scholarships & Benefits (Keep existing)
    first_graduate = Column(Boolean, default=False)
    pudhumai_pen = Column(Boolean, default=False)
    sc_st_scholarship = Column(Boolean, default=False)
    mbc_bc_scholarship = Column(Boolean, default=False)
    pmss_scholarship = Column(Boolean, default=False)
    category_7_5_scholarship = Column(Boolean, default=False)
    mudhalvan_scholarship = Column(Boolean, default=False)
    other_scholarship = Column(Boolean, default=False)
    other_scholarship_name = Column(String)

    # 4) Certificate Numbers (Keep existing)
    first_graduate_certificate_number = Column(String)
    income_certificate_number = Column(String)
    community_certificate_number = Column(String)
    aadhar_number = Column(String)

    # 5) Bank Account Details
    bank_name = Column(String)
    account_number = Column(String)
    ifsc_code = Column(String)
    bank_branch = Column(String)
    city = Column(String)
    account_type = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=True) # Linked User

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    description = Column(String, nullable=False)
    domains = Column(JSONB, nullable=False) # e.g. ["ai", "ml"]
    github_link = Column(String)
    created_at = Column(DateTime, server_default=func.now())

class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    description = Column(String, nullable=False)
    domains = Column(JSONB, nullable=False) # e.g. ["cyber", "cloud"]
    certificate_link = Column(String)
    created_at = Column(DateTime, server_default=func.now())

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    activity_type = Column(String, nullable=False) # "project_added", "cert_added"
    reference_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    seen_by_faculty = Column(Boolean, default=False)
