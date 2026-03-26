import sys
sys.path.append('.')
from database import SessionLocal
import models

with open('out_utf8.txt', 'w', encoding='utf-8') as f:
    db = SessionLocal()
    users = db.query(models.User).all()

    for u in users:
        f.write(f"ID: {u.id}, Username: '{u.username}', Email: '{u.email}'\n")
