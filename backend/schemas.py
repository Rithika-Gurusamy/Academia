from pydantic import BaseModel
from typing import Optional
from datetime import date

class UserBase(BaseModel):
    username: str
    email: str
    role: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    name: str
    register_no: str
    roll_no: Optional[str] = None
    mobile_no: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    scholar_type: Optional[str] = None
    blood_group: Optional[str] = None
    email_personal: Optional[str] = None
    email_college: Optional[str] = None
    residential_address: Optional[str] = None
    nationality: Optional[str] = None
    community: Optional[str] = None
    caste: Optional[str] = None
    religion: Optional[str] = None
    father_name: Optional[str] = None
    father_mobile_no: Optional[str] = None
    father_occupation: Optional[str] = None
    mother_name: Optional[str] = None
    mother_mobile_no: Optional[str] = None
    mother_occupation: Optional[str] = None
    guardian_name: Optional[str] = None
    guardian_mobile_no: Optional[str] = None
    guardian_occupation: Optional[str] = None
    family_annual_income: Optional[str] = None
    is_special_admission: Optional[str] = None
    is_differently_abled: Optional[str] = None

    umis_number: Optional[str] = None
    emis_number: Optional[str] = None
    academic_year_of_joining: Optional[str] = None
    course_type: Optional[str] = None
    branch_specialization: Optional[str] = None
    mode_of_study: Optional[str] = None
    type_of_admission: Optional[str] = None
    medium_of_instruction: Optional[str] = None
    date_of_admission: Optional[date] = None
    counselling_admission_number: Optional[str] = None

    first_graduate: Optional[bool] = False
    pudhumai_pen: Optional[bool] = False
    sc_st_scholarship: Optional[bool] = False
    mbc_bc_scholarship: Optional[bool] = False
    pmss_scholarship: Optional[bool] = False
    category_7_5_scholarship: Optional[bool] = False
    mudhalvan_scholarship: Optional[bool] = False
    other_scholarship: Optional[bool] = False
    other_scholarship_name: Optional[str] = None

    first_graduate_certificate_number: Optional[str] = None
    income_certificate_number: Optional[str] = None
    community_certificate_number: Optional[str] = None
    aadhar_number: Optional[str] = None

    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    bank_branch: Optional[str] = None
    city: Optional[str] = None
    account_type: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    # All fields optional for update
    name: Optional[str] = None
    register_no: Optional[str] = None
    roll_no: Optional[str] = None
    mobile_no: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    scholar_type: Optional[str] = None
    blood_group: Optional[str] = None
    email_personal: Optional[str] = None
    email_college: Optional[str] = None
    residential_address: Optional[str] = None
    nationality: Optional[str] = None
    community: Optional[str] = None
    caste: Optional[str] = None
    religion: Optional[str] = None
    father_name: Optional[str] = None
    father_mobile_no: Optional[str] = None
    father_occupation: Optional[str] = None
    mother_name: Optional[str] = None
    mother_mobile_no: Optional[str] = None
    mother_occupation: Optional[str] = None
    guardian_name: Optional[str] = None
    guardian_mobile_no: Optional[str] = None
    guardian_occupation: Optional[str] = None
    family_annual_income: Optional[str] = None
    is_special_admission: Optional[str] = None
    is_differently_abled: Optional[str] = None

    umis_number: Optional[str] = None
    emis_number: Optional[str] = None
    academic_year_of_joining: Optional[str] = None
    course_type: Optional[str] = None
    branch_specialization: Optional[str] = None
    mode_of_study: Optional[str] = None
    type_of_admission: Optional[str] = None
    medium_of_instruction: Optional[str] = None
    date_of_admission: Optional[date] = None
    counselling_admission_number: Optional[str] = None

    first_graduate: Optional[bool] = None
    pudhumai_pen: Optional[bool] = None
    sc_st_scholarship: Optional[bool] = None
    mbc_bc_scholarship: Optional[bool] = None
    pmss_scholarship: Optional[bool] = None
    category_7_5_scholarship: Optional[bool] = None
    mudhalvan_scholarship: Optional[bool] = None
    other_scholarship: Optional[bool] = None
    other_scholarship_name: Optional[str] = None

    first_graduate_certificate_number: Optional[str] = None
    income_certificate_number: Optional[str] = None
    community_certificate_number: Optional[str] = None
    aadhar_number: Optional[str] = None

    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    bank_branch: Optional[str] = None
    city: Optional[str] = None
    account_type: Optional[str] = None

class Student(StudentBase):
    id: int
    class_id: int

    class Config:
        from_attributes = True

from typing import List
from datetime import datetime

class ProjectBase(BaseModel):
    description: str
    domains: List[str]
    github_link: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    student_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CertificationBase(BaseModel):
    description: str
    domains: List[str]
    certificate_link: Optional[str] = None

class CertificationCreate(CertificationBase):
    pass

class Certification(CertificationBase):
    id: int
    student_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ActivityLog(BaseModel):
    id: int
    student_id: int
    activity_type: str
    reference_id: int
    created_at: datetime
    seen_by_faculty: bool
    student_name: Optional[str] = None 
    register_no: Optional[str] = None 
    description: Optional[str] = None
    domains: Optional[List[str]] = None
    link: Optional[str] = None

    class Config:
        from_attributes = True
