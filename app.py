from flask import Flask, request, send_file, render_template_string
from fpdf import FPDF
from docx import Document
import os
from datetime import datetime

app = Flask(__name__)

# Define file paths
WORD_FILE_PATH = "client_inquiry.docx"
PDF_FILE_PATH = "client_inquiry.pdf"
INQUIRIES_FOLDER = "inquiries"

# Ensure the inquiries folder exists
os.makedirs(INQUIRIES_FOLDER, exist_ok=True)

# Load the HTML form from the file directly in the same directory
def load_form_html():
    with open("index.html", "r") as file:
        return file.read()

# Helper function to get the current month's file path
def get_month_file():
    current_month = datetime.now().strftime('%Y-%m')
    month_file = os.path.join(INQUIRIES_FOLDER, f"{current_month}.txt")
    return month_file

# Route to display the form
@app.route('/')
def form():
    return render_template_string(load_form_html())

# Route to handle form submission and save inquiry data
@app.route('/save-inquiry', methods=['POST'])
def save_inquiry():
    client_name = request.form.get("client-name")
    phone_number = request.form.get("phone-number")
    client_inquiry = request.form.get("client-inquiry")
    booking_date = request.form.get("booking-date")
    resolution = request.form.get("resolution")
    date_called = request.form.get("date-called")
    feedback = request.form.get("client-feedback")
    conversion = request.form.get("conversion")

    # Get the current month file
    month_file = get_month_file()

    # Read existing inquiries to get the current count for numbering
    if os.path.exists(month_file):
        with open(month_file, "r") as file:
            inquiries = file.readlines()
    else:
        inquiries = []

    # Generate the inquiry entry
    inquiry_number = len(inquiries) + 1
    inquiry_entry = f"Enquiry #{inquiry_number}\n"
    inquiry_entry += f"Client Name: {client_name}\n"
    inquiry_entry += f"Phone Number: {phone_number}\n"
    inquiry_entry += f"Client Inquiry: {client_inquiry}\n"
    inquiry_entry += f"Booking Date: {booking_date}\n"
    inquiry_entry += f"Resolution: {resolution}\n"
    inquiry_entry += f"Date Client Was Called: {date_called}\n"
    inquiry_entry += f"Client Feedback: {feedback}\n"
    inquiry_entry += f"Conversion: {conversion}\n"
    inquiry_entry += "\n"  # Add space between entries

    # Save the new inquiry in the text file
    with open(month_file, "a") as file:
        file.write(inquiry_entry)

    # Create Word document
    doc = Document()
    doc.add_heading("Client Inquiry", level=1)
    doc.add_paragraph(f"Client Name: {client_name}")
    doc.add_paragraph(f"Phone Number: {phone_number}")
    doc.add_paragraph(f"Client Inquiry: {client_inquiry}")
    doc.add_paragraph(f"Booking Date: {booking_date}")
    doc.add_paragraph(f"Resolution: {resolution}")
    doc.add_paragraph(f"Date Client Was Called: {date_called}")
    doc.add_paragraph(f"Client Feedback: {feedback}")
    doc.add_paragraph(f"Conversion: {conversion}")
    doc.save(WORD_FILE_PATH)

    # Create PDF file
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Client Inquiry", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Client Name: {client_name}", ln=True)
    pdf.cell(200, 10, txt=f"Phone Number: {phone_number}", ln=True)
    pdf.cell(200, 10, txt=f"Client Inquiry: {client_inquiry}", ln=True)
    pdf.cell(200, 10, txt=f"Booking Date: {booking_date}", ln=True)
    pdf.cell(200, 10, txt=f"Resolution: {resolution}", ln=True)
    pdf.cell(200, 10, txt=f"Date Client Was Called: {date_called}", ln=True)
    pdf.cell(200, 10, txt=f"Client Feedback: {feedback}", ln=True)
    pdf.cell(200, 10, txt=f"Conversion: {conversion}", ln=True)
    pdf.output(PDF_FILE_PATH)

    # Success message with download links
    return f"""
    <div style="text-align: center; font-family: Arial;">
        <h3 style="color: #4CAF50;">Inquiry Submitted Successfully!</h3>
        <p>Thank you for submitting the inquiry for <strong>{client_name}</strong>.</p>
        <p>You can download the files below:</p>
        <a href="/download-word" style="color: #4CAF50;">Download Word File</a><br>
        <a href="/download-pdf" style="color: #4CAF50;">Download PDF File</a><br><br>
        <a href="/" style="color: #4CAF50;">Submit Another Inquiry</a>
    </div>
    """

# Route to download Word file
@app.route('/download-word')
def download_word():
    return send_file(WORD_FILE_PATH, as_attachment=True)

# Route to download PDF file
@app.route('/download-pdf')
def download_pdf():
    return send_file(PDF_FILE_PATH, as_attachment=True)

# Reset inquiries at the end of each month
def reset_inquiries():
    current_month = datetime.now().strftime('%Y-%m')
    month_file = os.path.join(INQUIRIES_FOLDER, f"{current_month}.txt")
    if os.path.exists(month_file):
        os.remove(month_file)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
