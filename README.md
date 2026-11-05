<div align="center">

# 🎓 Academia — Student Information Portal

**A full-stack student management system with role-based access, profile management, and real-time activity tracking**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Vercel](https://img.shields.io/badge/Frontend-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com)
[![Render](https://img.shields.io/badge/Backend-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![OpenSSF Scorecard](https://img.shields.io/badge/OpenSSF-Scorecard-brightgreen?style=for-the-badge)](https://securityscorecards.dev)

<br/>

> A modern, glassmorphic student portal where **students** manage their academic profiles, projects, and certifications — and **faculty** can search, filter, and monitor student activity in real time.

**🌐 Live Demo:** Frontend → [academia-five-dun.vercel.app](https://academia-five-dun.vercel.app) · Backend API → [academia-ci0l.onrender.com](https://academia-ci0l.onrender.com)

</div>

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [API Endpoints](#-api-endpoints)
- [Database Schema](#-database-schema)
- [Deployment](#-deployment)
- [Security](#-security)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔍 Overview

**Academia** is a comprehensive student information management system built for educational institutions. It provides separate interfaces for students and faculty with role-based authentication:

- **Students** can create and manage their detailed academic profiles (personal info, academic records, scholarships, bank details), add projects with GitHub links, and track certifications — all from a clean, responsive dashboard.
- **Faculty** can browse the full student directory, apply advanced multi-criteria filters (gender, scholar type, scholarship status, project/certification domains), and receive real-time notifications when students add new projects or certifications.

The application is fully deployed — frontend on **Vercel**, backend API on **Render**, with a managed **PostgreSQL** database.

---

## ✨ Features

### 🔐 Authentication & Account Recovery

| Feature | Description |
|---|---|
| **JWT Authentication** | Secure token-based auth with role claims (`student` / `faculty`) |
| **Role-Based Signup** | Separate registration for students and faculty |
| **Password Hashing** | Bcrypt-based password hashing via Passlib |
| **Forgot Password** | Email OTP-based password reset with 5-minute expiry |
| **Forgot Username** | OTP-verified username recovery with masked display |
| **OTP Rate Limiting** | Max 3 attempts per OTP; auto-cleanup of expired tokens |
| **Password Toggle** | Show/hide password visibility on all forms |

### 👨‍🎓 Student Portal

| Feature | Description |
|---|---|
| **Comprehensive Profile** | 50+ fields across 5 sections: General Info, Academic Info, Scholarships, Certificates, Bank Details |
| **Profile CRUD** | Create, view, edit, and save profile data with field-level validation |
| **View / Edit Mode Toggle** | Clean mode switching with visual badge indicators |
| **Projects Management** | Add projects with description, multi-domain tagging (18 domains), and GitHub links |
| **Certifications Management** | Add certifications with domain tags and certificate URLs |
| **Delete Entries** | Remove projects and certifications with confirmation |
| **Profile Ownership** | Students can only view and edit their own profiles |
| **Responsive Design** | Fully mobile-responsive glassmorphic UI |

### 👩‍🏫 Faculty Dashboard

| Feature | Description |
|---|---|
| **Student Directory** | Searchable list of all students by name or register number |
| **Advanced Filters** | 15+ filter criteria including register number range, gender, scholar type, scholarship booleans, and domain-based filtering |
| **Multi-Domain Filtering** | Filter students by project and certification domains (JSONB queries) |
| **Real-Time Activity Feed** | Notification sidebar with live polling (5s interval) for new student activity |
| **Activity Detail Modal** | Click any notification to view full details — description, domains, links |
| **Dismiss Notifications** | Mark activities as seen to clear the feed |
| **View Any Profile** | Faculty can view any student's complete profile |

### 🎨 UI / UX

| Feature | Description |
|---|---|
| **Glassmorphism Design** | Modern frosted-glass aesthetic with subtle gradients and blur effects |
| **Google Fonts (Outfit)** | Premium typography throughout the application |
| **Micro-Animations** | Smooth fade-ins, slide-ups, hover transforms, and pulse effects on CTAs |
| **Help Tip Bar** | Contextual guidance bar for first-time student users |
| **Adaptive Layouts** | Responsive grid systems that collapse gracefully on mobile |
| **Dark-on-Light Theme** | Green accent (#08CB00) color system with high-contrast text |

---

## 🛠 Tech Stack

### Backend

| Technology | Purpose |
|---|---|
| **Python 3.10+** | Core runtime |
| **FastAPI** | High-performance async API framework with auto-generated docs |
| **SQLAlchemy** | ORM for database models and queries |
| **PostgreSQL** | Primary relational database with JSONB support |
| **psycopg2** | PostgreSQL adapter for Python |
| **Pydantic** | Request/response schema validation with type safety |
| **python-jose** | JWT token creation and verification (HS256) |
| **Passlib + bcrypt** | Secure password hashing |
| **python-dotenv** | Environment variable management |
| **smtplib** | SMTP-based email delivery for OTP flows |
| **Uvicorn** | ASGI server for production deployment |

### Frontend

| Technology | Purpose |
|---|---|
| **HTML5** | Semantic page structure |
| **Vanilla CSS** | Custom styling with CSS variables, glassmorphism, and responsive media queries |
| **Vanilla JavaScript** | Client-side logic, API calls, DOM manipulation (zero frameworks) |
| **Google Fonts (Outfit)** | Modern typography |
| **Fetch API** | REST communication with Bearer token auth |
| **LocalStorage** | Client-side session persistence (token, role, username) |

### DevOps & Deployment

| Technology | Purpose |
|---|---|
| **Vercel** | Frontend hosting with speed insights and analytics |
| **Render** | Backend hosting with managed PostgreSQL |
| **GitHub Actions** | OpenSSF Scorecard supply-chain security analysis |
| **CORS Middleware** | Cross-origin resource sharing for Vercel ↔ Render communication |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                             │
│                    (Vercel — Static)                         │
│                                                             │
│   ┌──────────┐  ┌──────────────┐  ┌───────────────────┐    │
│   │ index    │  │  dashboard   │  │ faculty_dashboard  │    │
│   │ .html    │  │  .html       │  │ .html              │    │
│   │ Login /  │  │  Student     │  │ Directory /        │    │
│   │ Signup   │  │  Portal      │  │ Filters / Activity │    │
│   └────┬─────┘  └──────┬───────┘  └────────┬──────────┘    │
│        │               │                    │               │
│        └───────────────┼────────────────────┘               │
│                        │                                    │
│                   auth.js + style.css                        │
│                   profile.html                               │
└────────────────────────┼────────────────────────────────────┘
                         │ HTTPS (Bearer JWT)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                        BACKEND                              │
│                   (Render — FastAPI)                         │
│                                                             │
│   ┌────────────────────────────────────────────────────┐    │
│   │  main.py — API Routes                              │    │
│   │  ├── /signup, /login                               │    │
│   │  ├── /student/profile (CRUD)                       │    │
│   │  ├── /student/{reg}/projects (CRUD)                │    │
│   │  ├── /student/{reg}/certifications (CRUD)          │    │
│   │  ├── /student/list (filtered queries)              │    │
│   │  ├── /forgot-password, /forgot-username            │    │
│   │  ├── /verify-otp, /reset-password                  │    │
│   │  └── /faculty/activity-logs                        │    │
│   └──────────────────────┬─────────────────────────────┘    │
│                          │                                  │
│   ┌──────────┐  ┌────────┴───────┐  ┌──────────────────┐   │
│   │ auth.py  │  │  models.py     │  │  schemas.py      │   │
│   │ JWT +    │  │  SQLAlchemy    │  │  Pydantic        │   │
│   │ Bcrypt   │  │  ORM Models   │  │  Validation      │   │
│   └──────────┘  └────────┬───────┘  └──────────────────┘   │
│                          │                                  │
│                  ┌───────┴────────┐                         │
│                  │  database.py   │                         │
│                  │  Engine +      │                         │
│                  │  Session       │                         │
│                  └───────┬────────┘                         │
└──────────────────────────┼──────────────────────────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │   PostgreSQL    │
                  │   (Render DB)   │
                  │                 │
                  │  users          │
                  │  students       │
                  │  projects       │
                  │  certifications │
                  │  activity_logs  │
                  │  otps           │
                  └─────────────────┘
```

---

## 📁 Project Structure

```
sem6/
│
├── backend/
│   ├── main.py                # FastAPI application — all API routes
│   ├── models.py              # SQLAlchemy ORM models (User, Student, Project, Certification, OTP, ActivityLog)
│   ├── schemas.py             # Pydantic validation schemas (Create, Update, Response models)
│   ├── database.py            # Database engine & session configuration
│   ├── auth.py                # JWT token creation/verification + bcrypt password hashing
│   ├── requirements.txt       # Backend Python dependencies
│   ├── migrate_db.py          # Database migration utility
│   ├── check_db.py            # Database connection health check
│   └── .env                   # Environment variables (gitignored)
│
├── frontend/
│   ├── index.html             # Login / Signup / Account Recovery page
│   ├── dashboard.html         # Student dashboard — profile lookup, projects, certifications
│   ├── faculty_dashboard.html # Faculty dashboard — student directory, filters, activity feed
│   ├── profile.html           # Detailed student profile — view / edit / create mode
│   ├── auth.js                # Authentication logic — login, signup, OTP recovery flows
│   └── style.css              # Global stylesheet — glassmorphism design system
│
├── .github/
│   └── workflows/
│       └── scorecard.yml      # OpenSSF Scorecard supply-chain security CI
│
├── requirements.txt           # Root-level dependencies (mirrors backend)
├── test_signup.py             # Signup integration test
├── clean_dump.sql             # Database schema dump (gitignored)
├── .gitignore
└── LICENSE                    # MIT License
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **PostgreSQL 14+** (local or managed)
- **Git**

### 1. Clone the Repository

```bash
git clone https://github.com/Rithika-Gurusamy/trace.git
cd trace
```

### 2. Set Up the Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\Activate          # Windows PowerShell

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `backend/.env` file:

```env
# PostgreSQL connection string
DATABASE_URL=postgresql://username:password@localhost:5432/academia_db

# JWT secret key (change in production!)
JWT_SECRET_KEY=your-secret-key-here

# Email config for OTP (Gmail App Password recommended)
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
```

### 4. Initialize the Database

```bash
# PostgreSQL should be running
# Tables auto-create on first startup via SQLAlchemy
```

### 5. Run the Backend

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### 6. Run the Frontend

Open `frontend/index.html` directly in a browser or serve it locally:

```bash
# Using Python's built-in server
cd frontend
python -m http.server 5500
```

Then open `http://localhost:5500` in your browser.

> **Note:** Update the `API_URL` constant in `auth.js`, `dashboard.html`, `faculty_dashboard.html`, and `profile.html` to point to your local backend (`http://localhost:8000`) instead of the production Render URL.

---

## 🔌 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `POST` | `/signup` | Register a new user (student/faculty) | ❌ |
| `POST` | `/login` | Login and receive JWT token | ❌ |

### Account Recovery

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `POST` | `/forgot-password` | Send OTP to email for password reset | ❌ |
| `POST` | `/forgot-username` | Send OTP to email for username recovery | ❌ |
| `POST` | `/verify-otp` | Verify the 6-digit OTP | ❌ |
| `POST` | `/reset-password` | Reset password with verified OTP | ❌ |
| `POST` | `/retrieve-username` | Retrieve username with verified OTP | ❌ |

### Student Profiles

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `POST` | `/student/profile` | Create student profile (own only) | 🔒 Student |
| `GET` | `/student/profile/{register_no}` | View profile (own or faculty) | 🔒 Student/Faculty |
| `PUT` | `/student/profile/{register_no}` | Update profile (own or faculty) | 🔒 Student/Faculty |
| `GET` | `/student/list` | List students with advanced filters | 🔒 Faculty |

### Projects & Certifications

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `POST` | `/student/{reg}/projects` | Add a project | 🔒 Student |
| `GET` | `/student/{reg}/projects` | List projects | 🔒 Student/Faculty |
| `DELETE` | `/student/projects/{id}` | Delete a project | 🔒 Student |
| `POST` | `/student/{reg}/certifications` | Add a certification | 🔒 Student |
| `GET` | `/student/{reg}/certifications` | List certifications | 🔒 Student/Faculty |
| `DELETE` | `/student/certifications/{id}` | Delete a certification | 🔒 Student |

### Faculty Activity

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/faculty/activity-logs` | Get unseen activity logs | 🔒 Faculty |
| `POST` | `/faculty/activity-logs/{id}/seen` | Dismiss a notification | 🔒 Faculty |

---

## 🗄 Database Schema

```mermaid
erDiagram
    USERS {
        int id PK
        string username UK
        string email UK
        string password_hash
        string role
    }

    STUDENTS {
        int id PK
        int user_id FK
        string name
        string register_no UK
        string roll_no
        string mobile_no
        date date_of_birth
        string gender
        string scholar_type
        string blood_group
        string community
        string father_name
        string mother_name
        boolean first_graduate
        boolean pudhumai_pen
        boolean sc_st_scholarship
        string bank_name
        string account_number
        string ifsc_code
    }

    PROJECTS {
        int id PK
        int student_id FK
        string description
        jsonb domains
        string github_link
        datetime created_at
    }

    CERTIFICATIONS {
        int id PK
        int student_id FK
        string description
        jsonb domains
        string certificate_link
        datetime created_at
    }

    ACTIVITY_LOGS {
        int id PK
        int student_id FK
        string activity_type
        int reference_id
        datetime created_at
        boolean seen_by_faculty
    }

    OTPS {
        int id PK
        string email
        string otp_code
        int expires_at
        int attempts
    }

    USERS ||--o| STUDENTS : "has profile"
    STUDENTS ||--o{ PROJECTS : "owns"
    STUDENTS ||--o{ CERTIFICATIONS : "owns"
    STUDENTS ||--o{ ACTIVITY_LOGS : "generates"
```

---

## 🚢 Deployment

### Frontend (Vercel)

The `frontend/` directory is deployed as a static site on Vercel:

1. Connect your GitHub repository to Vercel
2. Set the **Root Directory** to `frontend`
3. No build step required — purely static HTML/CSS/JS
4. Vercel Speed Insights and Web Analytics are integrated

### Backend (Render)

The `backend/` directory is deployed as a Web Service on Render:

1. Connect your GitHub repository to Render
2. Set the **Root Directory** to `backend`
3. **Build Command:** `pip install -r requirements.txt`
4. **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables: `DATABASE_URL`, `JWT_SECRET_KEY`, `SENDER_EMAIL`, `SENDER_PASSWORD`
6. Render provides a managed PostgreSQL database — copy its internal URL as `DATABASE_URL`

### CI / CD

- **OpenSSF Scorecard** runs automatically on pushes to `main` via GitHub Actions, assessing supply-chain security practices

---

## 🔒 Security

| Practice | Implementation |
|---|---|
| **Password Hashing** | Bcrypt via Passlib (auto-salted, configurable rounds) |
| **JWT Tokens** | HS256 signed, 24-hour expiry, user_id + role embedded |
| **OTP Security** | 6-digit codes, 5-minute expiry, max 3 attempts, server-side cleanup |
| **Authorization** | Students can only access their own profile; faculty has read-all access |
| **CORS** | Whitelisted origins only (Vercel production + localhost dev) |
| **Secrets** | API keys and DB credentials in `.env` (gitignored), never in source |
| **Input Validation** | Pydantic schema enforcement on all request bodies |
| **Supply Chain** | OpenSSF Scorecard CI for dependency and workflow security |
| **XSS Prevention** | `textContent` used over `innerHTML` for dynamic content rendering |

> ⚠️ **Important:** Never commit `.env` files or API keys. Rotate any secrets that were accidentally exposed.

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built by [Rithika Gurusamy](https://github.com/Rithika-Gurusamy)**

*Academia — Simplifying student data management for educational institutions*

</div>
