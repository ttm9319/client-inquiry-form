from flask import Flask, request, render_template_string
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from datetime import datetime
import os

# Load environment variables from .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Initialize Flask app
app = Flask(__name__)

# Database setup
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Define the Inquiry model
class Inquiry(Base):
    __tablename__ = 'inquiries'
    id = Column(Integer, primary_key=True)
    client_name = Column(String(100))
    phone_number = Column(String(20))
    client_inquiry = Column(Text)
    booking_date = Column(String(20))
    resolution = Column(Text)
    date_called = Column(String(20))
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
    return '''
    <form action="/save-inquiry" method="post">
        <label>Client Name: <input type="text" name="client-name"></label><br>
        <label>Phone Number: <input type="text" name="phone-number"></label><br>
        <label>Inquiry: <textarea name="client-inquiry"></textarea></label><br>
        <label>Booking Date: <input type="text" name="booking-date"></label><br>
        <label>Resolution: <input type="text" name="resolution"></label><br>
        <label>Date Called: <input type="text" name="date-called"></label><br>
        <label>Feedback: <textarea name="client-feedback"></textarea></label><br>
        <label>Conversion: <input type="text" name="conversion"></label><br>
        <button type="submit">Submit Inquiry</button>
    </form>
    '''

# Route to handle form submission and save inquiry
@app.route('/save-inquiry', methods=['POST'])
def save_inquiry():
    # Get form data
    client_name = request.form['client-name']
    phone_number = request.form['phone-number']
    client_inquiry = request.form['client-inquiry']
    booking_date = request.form['booking-date']
    resolution = request.form['resolution']
    date_called = request.form['date-called']
    feedback = request.form['client-feedback']
    conversion = request.form['conversion']
    
    # Save to database
    session = Session()
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
    session = Session()
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
