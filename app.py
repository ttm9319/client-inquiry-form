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

    # Return a detailed success message with a link to submit another inquiry
    return """
    <h3>Inquiry Submitted Successfully!</h3>
    <p>Thank you for submitting the inquiry for <strong>{}</strong>.</p>
    <p>You can download the generated files below:</p>
    <ul>
        <li><a href="/download-word">Download Word File</a></li>
        <li><a href="/download-pdf">Download PDF File</a></li>
    </ul>
    <p><a href="/">Click here to submit another inquiry</a></p>
    """.format(client_name)
