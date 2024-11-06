from flask import Flask, request, render_template
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from datetime import datetime
import os

# Load environment variables from .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Ensure the database URL is available
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Initialize Flask app
app = Flask(__name__)

# Database setup with SSL if necessary
engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Define the Inquiry model
class Inquiry(Base):
    __tablename__ = 'inquiries'
    id = Column(Integer, primary_key=True)
    client_name = Column(String(100))
    phone_number = Column(String(20))
    client_inquiry = Column(Text)
    booking_date = Column(DateTime)
    resolution = Column(Text)
    date_called = Column(DateTime)
    feedback = Column(Text)
    conversion = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)

# Route to create database tables (temporary, remove after setup)
@app.route('/create-db')
def create_db():
    Base.metadata.create_all(bind=engine)
    return "Database tables created!"

# Route to display the form
@app.route('/')
def form():
    return render_template("index.html")

# Route to handle form submission and save inquiry
@app.route('/save-inquiry', methods=['POST'])
def save_inquiry():
    # Get form data
    client_name = request.form['client-name']
    phone_number = request.form['phone-number']
    client_inquiry = request.form['client-inquiry']
    booking_date = datetime.strptime(request.form['booking-date'], '%Y-%m-%d')  # Convert to datetime
    resolution = request.form['resolution']
    date_called = datetime.strptime(request.form['date-called'], '%Y-%m-%d') if request.form['date-called'] else None  # Convert to datetime
    feedback = request.form['client-feedback']
    conversion = request.form['conversion']
    
    # Use context manager for session handling
    with Session() as session:
        new_inquiry = Inquiry(
            client_name=client_name,
            phone_number=phone_number,
            client_inquiry=client_inquiry,
            booking_date=booking_date,
            resolution=resolution,
            date_called=date_called,
            feedback=feedback,
            conversion=conversion
        )
        session.add(new_inquiry)
        session.commit()

    return '''
    <h3>Inquiry Submitted Successfully!</h3>
    <a href="/inquiries">View All Inquiries</a><br>
    <a href="/">Submit Another Inquiry</a>
    '''

# Route to display inquiries in descending order
@app.route('/inquiries')
def inquiries():
    with Session() as session:
        inquiries = session.query(Inquiry).order_by(Inquiry.created_at.desc()).all()
        output = "<h1>All Inquiries</h1><ul>"
        for inquiry in inquiries:
            output += f"<li>Inquiry #{inquiry.id}: {inquiry.client_name} - {inquiry.client_inquiry[:50]}...</li>"
        output += "</ul><br><a href='/'>Submit Another Inquiry</a>"
    return output

# Run the app
if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))  # Use PORT env variable if available, otherwise default to 8080
    app.run(host='0.0.0.0', port=port, debug=True)
