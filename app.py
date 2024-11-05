from flask import Flask, request, jsonify, send_file, render_template_string
from docx import Document
from fpdf import FPDF
import os

app = Flask(__name__)

# Paths to save the generated files
WORD_FILE_PATH = "inquiry.docx"
PDF_FILE_PATH = "inquiry.pdf"

# HTML content for index page
index_html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Client Inquiry Form</title>
</head>
<body>
    <h1>Client Inquiry Form</h1>
    <form action="/save-inquiry" method="POST">
        <label for="client-name">Client Name:</label>
        <input type="text" id="client-name" name="client-name"><br><br>

        <label for="phone-number">Phone Number:</label>
        <input type="text" id="phone-number" name="phone-number"><br><br>

        <label for="client-inquiry">Client Inquiry:</label>
        <textarea id="client-inquiry" name="client-inquiry"></textarea><br><br>

        <label for="booking-date">Booking Date:</label>
        <input type="date" id="booking-date" name="booking-date"><br><br>

        <label for="client-resolution">Client Resolution:</label>
        <textarea id="client-resolution" name="client-resolution"></textarea><br><br>

        <label for="date-called">Date Client Was Called:</label>
        <input type="date" id="date-called" name="date-called"><br><br>

        <label for="client-feedback">Client Feedback:</label>
        <textarea id="client-feedback" name="client-feedback"></textarea><br><br>

        <label for="conversion">Conversion (Booked or Not):</label>
        <select id="conversion" name="conversion">
            <option value="Booked">Booked</option>
            <option value="Not Booked">Not Booked</option>
        </select><br><br>

        <button type="submit">Submit Inquiry</button>
    </form>
</body>
</html>
"""

# Route to display the HTML form
@app.route('/')
def form():
    return render_template_string(index_html_content)

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
    pdf.cell(200, 10, txt=f"Phone Number: {phone_number}", ln=True)
    pdf.cell(200, 10, txt=f"Client Inquiry: {client_inquiry}", ln=True)
    pdf.cell(200, 10, txt=f"Booking Date: {booking_date}", ln=True)
    pdf.cell(200, 10, txt=f"Client Resolution: {client_resolution}", ln=True)
    pdf.cell(200, 10, txt=f"Date Client Was Called: {date_called}", ln=True)
    pdf.cell(200, 10, txt=f"Client Feedback: {client_feedback}", ln=True)
    pdf.cell(200, 10, txt=f"Conversion: {conversion}", ln=True)
    pdf.output(PDF_FILE_PATH)

    return jsonify({"success": True})

# Route to download files
@app.route('/download-files')
def download_files():
    return f"""
    <h3>Download Files</h3>
    <ul>
        <li><a href="/download-word">Download Word File</a></li>
        <li><a href="/download-pdf">Download PDF File</a></li>
    </ul>
    """

@app.route('/download-word')
def download_word():
    return send_file(WORD_FILE_PATH, as_attachment=True)

@app.route('/download-pdf')
def download_pdf():
    return send_file(PDF_FILE_PATH, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
