from flask import Flask, request, send_file
from fpdf import FPDF
from docx import Document
import os

app = Flask(__name__)

# Define file paths
WORD_FILE_PATH = "client_inquiry.docx"
PDF_FILE_PATH = "client_inquiry.pdf"

# Home route to display the form
@app.route('/')
def form():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Client Inquiry Form</title>
    </head>
    <body>
        <form action="/save-inquiry" method="POST">
            <label for="client-name">Client Name:</label>
            <input type="text" id="client-name" name="client-name" required><br>
            <label for="phone-number">Phone Number:</label>
            <input type="text" id="phone-number" name="phone-number" required><br>
            <label for="client-inquiry">Client Inquiry:</label>
            <textarea id="client-inquiry" name="client-inquiry" required></textarea><br>
            <label for="booking-date">Booking Date:</label>
            <input type="date" id="booking-date" name="booking-date" required><br>
            <label for="conversion">Conversion (Booked or Not):</label>
            <select id="conversion" name="conversion" required>
                <option value="Booked">Booked</option>
                <option value="Not Booked">Not Booked</option>
            </select><br>
            <button type="submit">Submit Inquiry</button>
        </form>
    </body>
    </html>
    """

# Route to handle form submission and save inquiry data
@app.route('/save-inquiry', methods=['POST'])
def save_inquiry():
    client_name = request.form.get("client-name")
    phone_number = request.form.get("phone-number")
    client_inquiry = request.form.get("client-inquiry")
    booking_date = request.form.get("booking-date")
    conversion = request.form.get("conversion")

    # Create Word document
    doc = Document()
    doc.add_heading("Client Inquiry", level=1)
    doc.add_paragraph(f"Client Name: {client_name}")
    doc.add_paragraph(f"Phone Number: {phone_number}")
    doc.add_paragraph(f"Client Inquiry: {client_inquiry}")
    doc.add_paragraph(f"Booking Date: {booking_date}")
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
