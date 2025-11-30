# Script to seed initial data
from app.db.session import SessionLocal
# from app.models.user import User

def seed_data():
    db = SessionLocal()
    # Add seed logic here
    db.close()

if __name__ == "__main__":
    seed_data()
