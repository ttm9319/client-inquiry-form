from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Date, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

app = Flask(__name__)

# Database configuration
DATABASE_URL = 'postgresql://ttm_user:SIq7GRpfyQjenTuJf6tn3NTz2GLK2sHj@dpg-cslidvjv2p9s7386g01g-a.oregon-postgres.render.com/ttm'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the base for SQLAlchemy models
Base = declarative_base()

# Define the Inquiry model
class Inquiry(Base):
    __tablename__ = 'inquiries'

    id = Column(Integer, primary_key=True)
    client_name = Column(String(255))
    phone_number = Column(String(20))
    client_inquiry = Column(Text)
    booking_date = Column(Date)
    resolution = Column(Text)
    date_called = Column(Date)
    feedback = Column(Text)
    conversion = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables at startup if they don't exist
with engine.connect() as connection:
    Base.metadata.create_all(bind=engine)

# Sample route to add an inquiry (example)
@app.route('/add_inquiry', methods=['POST'])
def add_inquiry():
    data = request.get_json()
    session = SessionLocal()
    try:
        new_inquiry = Inquiry(
            client_name=data['client_name'],
            phone_number=data['phone_number'],
            client_inquiry=data['client_inquiry'],
            booking_date=data['booking_date'],
            resolution=data['resolution'],
            date_called=data['date_called'],
            feedback=data['feedback'],
            conversion=data['conversion'],
            created_at=datetime.utcnow()
        )
        session.add(new_inquiry)
        session.commit()
        return jsonify({"message": "Inquiry added successfully!"}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@app.route('/')
def home():
    return "Welcome to the Inquiry App!"

if __name__ == '__main__':
    app.run(debug=True)
