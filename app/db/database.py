from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.models.models import User
from passlib.hash import bcrypt
from app.dependencies.utils import get_password_hash
from app.db.base import Base

# Database URL
DATABASE_URL = "postgresql://user:password@db:5432/fastapi_db"

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables_and_populate():
    from app.models.models import Suburb  # Import moved here to avoid circular imports
    from app.data.suburb import suburbs  # Import moved here if it only contains data
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Ensure the admin user exists
        admin_user = db.query(User).filter(User.username == "martin@infinitech.co.nz").first()
        if not admin_user:
            print("Creating admin user...")
            hashed_password = get_password_hash("Mannuthy123@")
            admin_user = User(
                username="martin@infinitech.co.nz",
                email="martin@infinitech.co.nz",
                hashed_password=hashed_password,
                is_superuser=True,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("Admin user created successfully.")
        else:
            print("Admin user already exists.")

        # Populate the Suburb table
        existing_suburbs = db.query(Suburb).first()  # Check if there is at least one record
        if not existing_suburbs:
            print("Populating suburbs table...")
            for suburb_data in suburbs:
                suburb = Suburb(
                    name=suburb_data["name"],
                    city=suburb_data["city"],
                    region=suburb_data["region"],
                    postcode=suburb_data["postcode"]
                )
                db.add(suburb)
            db.commit()
            print("Suburbs table populated successfully.")
        else:
            print("Suburbs table already populated.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
