from flask import Flask, request, jsonify, send_file, render_template
from docx import Document
from fpdf import FPDF
import os

app = Flask(__name__)

# Paths to save the generated files
WORD_FILE_PATH = "inquiry.docx"
PDF_FILE_PATH = "inquiry.pdf"

# Route to display the HTML form
@app.route('/')
def form():
    return render_template('index.html')

# Route to save inquiry data and generate files
@app.route('/save-inquiry', methods=['POST'])
def save_inquiry():
    # Get form data
    client_name = request.form.get("client-name")
    phone_number = request.form.get("phone-number")
    client_inquiry = request.form.get("client-inquiry")
    booking_date = request.form.get("booking-date")
    client_resolution = request.form.get("client-resolution")
    date_called = request.form.get("date-called")
    client_feedback = request.form.get("client-feedback")
    conversion = request.form.get("conversion")

    # Create or update Word document
    doc = Document()
    doc.add_heading("Client Inquiry", level=1)
    doc.add_paragraph(f"Client Name: {client_name}")
    doc.add_paragraph(f"Phone Number: {phone_number}")
    doc.add_paragraph(f"Client Inquiry: {client_inquiry}")
    doc.add_paragraph(f"Booking Date: {booking_date}")
    doc.add_paragraph(f"Client Resolution: {client_resolution}")
    doc.add_paragraph(f"Date Client Was Called: {date_called}")
    doc.add_paragraph(f"Client Feedback: {client_feedback}")
    doc.add_paragraph(f"Conversion: {conversion}")
    doc.save(WORD_FILE_PATH)

    # Convert Word content to PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Client Inquiry", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Client Name: {client_name}", ln=True)
    pdf.cell(200, 10, txt=f"
