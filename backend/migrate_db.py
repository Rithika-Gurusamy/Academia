from database import engine
from sqlalchemy import text

with engine.connect() as conn:
    # Add email column to users if it doesn't exist
    try:
        conn.execute(text("ALTER TABLE users ADD COLUMN email VARCHAR(255)"))
        conn.commit()
        print("Added email column to users table.")
    except Exception as e:
        print(f"Could not add email column (it might already exist): {e}")

    # Create otps table
    try:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS otps (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                otp_code VARCHAR(6) NOT NULL,
                expires_at INTEGER NOT NULL,
                attempts INTEGER DEFAULT 0
            )
        """))
        conn.commit()
        print("Created otps table.")
    except Exception as e:
        print(f"Error creating otps table: {e}")

    # Add user_id column to students
    try:
        conn.execute(text("ALTER TABLE students ADD COLUMN user_id INTEGER REFERENCES users(id) UNIQUE"))
        conn.commit()
        print("Added user_id column to students table.")
    except Exception as e:
        print(f"Could not add user_id column (it might already exist): {e}")
