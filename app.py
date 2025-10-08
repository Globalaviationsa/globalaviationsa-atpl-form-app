from flask import Flask, render_template, request
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfReader, PdfWriter
import os, datetime, smtplib
from email.message import EmailMessage

app = Flask(__name__)

# Your pre-filled template PDF (must be in the same folder as this app.py)
TEMPLATE_MAP = {
    "Integrated_Old": "Application ATPL Fillable_Generic_ATPL.pdf",
    "Modular_Old": "Application ATPL Fillable_Generic_Modular.pdf",
    "Feb_2025": "Application ATPL Fillable_Feb_2025_3rd_Trimester.pdf",
    "Mar_A3_2025": "Application ATPL Fillable_Aegean_2025_3rd_Trimester.pdf",
    "Jun_2025": "Application ATPL Fillable_June_2025_2nd_Trimester.pdf",
    "Sep_2025": "Application ATPL Fillable_Sep_2025_1st_Trimester.pdf"
}
OUTPUT_DIR = "filled_pdfs"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- PDF FILL FUNCTION ---
def fill_pdf(student_data, output_filename):
    overlay_path = "overlay.pdf"
    c = canvas.Canvas(overlay_path, pagesize=A4)

    # --- Page 1 : Personal Details (Section 1) ---
    c.setFont("Helvetica", 9)
    c.drawString(75, 608, student_data["surname"].upper())
    c.drawString(350, 608, student_data["firstname"].upper())
    c.drawString(125, 588.5, student_data["title"].upper())
    c.drawString(405, 588.5, student_data["dob"].upper())
    c.drawString(78, 570, student_data["nationality"].upper())
    c.drawString(380, 570, student_data["birthplace_town"].upper())
    c.drawString(488, 570, student_data["birthplace_country"].upper())
    c.drawString(120, 550, student_data["address"].upper())
    c.drawString(335, 531, student_data["postcode"].upper())
    c.drawString(100, 511, student_data["phone"].upper())
    c.drawString(358, 511, student_data["mobile"].upper())
    c.drawString(100, 492, student_data["email"])

    # --- Page 1 : Section 3 (Date) ---
    c.setFont("Helvetica", 10)
    c.drawString(330, 214, student_data["declaration_date"])  # adjust coords

    # --- Move to Page 2 ---
    c.showPage()
    c.setFont("Helvetica", 10)

    # --- Page 2 : Section 5 (Subjects + Attempts + Dates) ---
    c.drawString(345, 646, student_data["airlaw_attempt1"])
    c.drawString(382, 646, student_data["airlaw_attempt2"])
    c.drawString(418, 646, student_data["airlaw_attempt3"])
    c.drawString(453, 646, student_data["airlaw_attempt4"])
    c.drawString(480, 646, student_data["airlaw_date"])

    c.drawString(345, 630, student_data["agk_asp_attempt1"])
    c.drawString(382, 630, student_data["agk_asp_attempt2"])
    c.drawString(418, 630, student_data["agk_asp_attempt3"])
    c.drawString(453, 630, student_data["agk_asp_attempt4"])
    c.drawString(480, 630, student_data["agk_asp_date"])

    c.drawString(345, 614, student_data["agk_i_attempt1"])
    c.drawString(382, 614, student_data["agk_i_attempt2"])
    c.drawString(418, 614, student_data["agk_i_attempt3"])
    c.drawString(453, 614, student_data["agk_i_attempt4"])
    c.drawString(480, 614, student_data["agk_i_date"])

    c.drawString(345, 597, student_data["mb_attempt1"])
    c.drawString(382, 597, student_data["mb_attempt2"])
    c.drawString(418, 597, student_data["mb_attempt3"])
    c.drawString(453, 597, student_data["mb_attempt4"])
    c.drawString(480, 597, student_data["mb_date"])

    c.drawString(345, 581, student_data["perf_attempt1"])
    c.drawString(382, 581, student_data["perf_attempt2"])
    c.drawString(418, 581, student_data["perf_attempt3"])
    c.drawString(453, 581, student_data["perf_attempt4"])
    c.drawString(480, 581, student_data["perf_date"])

    c.drawString(345, 565, student_data["fpm_attempt1"])
    c.drawString(382, 565, student_data["fpm_attempt2"])
    c.drawString(418, 565, student_data["fpm_attempt3"])
    c.drawString(453, 565, student_data["fpm_attempt4"])
    c.drawString(480, 565, student_data["fpm_date"])

    c.drawString(345, 548, student_data["hpl_attempt1"])
    c.drawString(382, 548, student_data["hpl_attempt2"])
    c.drawString(418, 548, student_data["hpl_attempt3"])
    c.drawString(453, 548, student_data["hpl_attempt4"])
    c.drawString(480, 548, student_data["hpl_date"])

    c.drawString(345, 532, student_data["met_attempt1"])
    c.drawString(382, 532, student_data["met_attempt2"])
    c.drawString(418, 532, student_data["met_attempt3"])
    c.drawString(453, 532, student_data["met_attempt4"])
    c.drawString(480, 532, student_data["met_date"])

    c.drawString(345, 516, student_data["gnav_attempt1"])
    c.drawString(382, 516, student_data["gnav_attempt2"])
    c.drawString(418, 516, student_data["gnav_attempt3"])
    c.drawString(453, 516, student_data["gnav_attempt4"])
    c.drawString(480, 516, student_data["gnav_date"])

    c.drawString(345, 500, student_data["rnav_attempt1"])
    c.drawString(382, 500, student_data["rnav_attempt2"])
    c.drawString(418, 500, student_data["rnav_attempt3"])
    c.drawString(453, 500, student_data["rnav_attempt4"])
    c.drawString(480, 500, student_data["rnav_date"])

    c.drawString(345, 484, student_data["ops_attempt1"])
    c.drawString(382, 484, student_data["ops_attempt2"])
    c.drawString(418, 484, student_data["ops_attempt3"])
    c.drawString(453, 484, student_data["ops_attempt4"])
    c.drawString(480, 484, student_data["ops_date"])

    c.drawString(345, 468, student_data["pof_attempt1"])
    c.drawString(382, 468, student_data["pof_attempt2"])
    c.drawString(418, 468, student_data["pof_attempt3"])
    c.drawString(453, 468, student_data["pof_attempt4"])
    c.drawString(480, 468, student_data["pof_date"])

    c.drawString(345, 452, student_data["comm_attempt1"])
    c.drawString(382, 452, student_data["comm_attempt2"])
    c.drawString(418, 452, student_data["comm_attempt3"])
    c.drawString(453, 452, student_data["comm_attempt4"])
    c.drawString(480, 452, student_data["comm_date"])

    # Total Exams
    c.drawString(345, 436, student_data["total_exams"])

    # --- Page 2 : Section 5 (Date) ---
    c.setFont("Helvetica", 10)
    c.drawString(310, 130, student_data["declaration_date"])  # adjust coords

    # --- Move to Page 3 ---
    c.showPage()
    c.setFont("Helvetica", 10)

    # --- Page 3 : Declaration ---
    c.drawString(70, 421, student_data["declaration_signature"].upper())
    c.drawString(315, 421, student_data["declaration_date"])

    c.save()

    # --- MERGE WITH TEMPLATE ---
    template = PdfReader(open(student_data["template_pdf"], "rb"))
    overlay = PdfReader(open(overlay_path, "rb"))
    writer = PdfWriter()

    for i, page in enumerate(template.pages):
        if i < len(overlay.pages):
            page.merge_page(overlay.pages[i])
        writer.add_page(page)

    with open(os.path.join(OUTPUT_DIR, output_filename), "wb") as f:
        writer.write(f)

# --- HELPER FUNCTION TO EMAIL PDFs ---
# --- HELPER FUNCTION TO EMAIL PDFs TO ADMIN + STUDENT ---
def send_emails(pdf_path, student_email):
    try:
        subject = os.path.splitext(os.path.basename(pdf_path))[0]  # same as PDF name

        # --- Admin email (with PDF attached) ---
        admin_msg = EmailMessage()
        admin_msg["Subject"] = subject
        admin_msg["From"] = os.environ["EMAIL_USER"]                  # exams@globalaviationsa.com
        admin_msg["To"] = "exams@globalaviationsa.com"                # receive at exams inbox
        admin_msg.set_content("Attached is a completed ATPL application form.")
        with open(pdf_path, "rb") as f:
            admin_msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="pdf",
                filename=os.path.basename(pdf_path)
            )

        # --- Student email (no attachment) ---
        student_msg = EmailMessage()
        student_msg["Subject"] = subject
        student_msg["From"] = os.environ["EMAIL_USER"]                # send from exams@
        student_msg["To"] = student_email
        student_msg.set_content(
            "Dear Student,\n\n"
            "Your email has been successfully received.\n\n"
            "Please make sure to check FlightLogger regularly for important updates and deadlines.\n\n"
            "Once your application is submitted to the HCAA, you will be able to view it in your profile under:\n\n"
            "Documents > HCAA Exams\n\n"
            "If there is any issue with your application, we will contact you directly.\n\n"
            "After the examination period, please collect your PDF results and send them in a single email to: exams@globalaviationsa.com. \n\n"
            "We are here to support you throughout the process. Should you have any questions or need assistance, please don't hesitate to reach out."
        )

        # --- Send both via SMTP (one connection) ---
        with smtplib.SMTP("mail.globalaviationsa.com", 587) as smtp:
            smtp.starttls()
            smtp.login(os.environ["EMAIL_USER"], os.environ["EMAIL_PASS"])
            smtp.send_message(admin_msg)
            smtp.send_message(student_msg)

        print("✅ Admin + Student emails sent.")
    except Exception as e:
        print("❌ Email error:", e)

# --- WEB ROUTE ---
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # --- REQUIRED FIELD VALIDATION ---
        if not request.form["surname"] or not request.form["firstname"] or not request.form["title"] \
           or not request.form["dob"] or not request.form["nationality"] \
           or not request.form["birthplace_town"] or not request.form["birthplace_country"] \
           or not request.form["address"] or not request.form["postcode"] \
           or not request.form["mobile"] or not request.form["email"] \
           or not request.form["declaration_signature"]:
            return "Error: You must fill all required fields in Section 1 Personal Details as well as Section 7 Declaration", 400

	# --- Class Selection ---
        selected_class = request.form["class_selection"]
        if selected_class not in TEMPLATE_MAP:
            return "Error: Invalid class selected.", 400
        template_pdf = TEMPLATE_MAP[selected_class]
        
        # --- COLLECT DATA ---
        data = {
            "surname": request.form["surname"],
            "firstname": request.form["firstname"],
            "title": request.form["title"],
            "dob": datetime.datetime.strptime(request.form["dob"], "%Y-%m-%d").strftime("%d/%m/%Y"),
            "nationality": request.form["nationality"],
            "birthplace_town": request.form["birthplace_town"],
            "birthplace_country": request.form["birthplace_country"],
            "address": request.form["address"],
            "postcode": request.form["postcode"],
            "phone": request.form["phone"],
            "mobile": request.form["mobile"],
            "email": request.form["email"],
            "template_pdf": template_pdf,

            # --- Subjects ---
            "airlaw_attempt1": "✓" if "airlaw_attempt1" in request.form else "",
            "airlaw_attempt2": "✓" if "airlaw_attempt2" in request.form else "",
            "airlaw_attempt3": "✓" if "airlaw_attempt3" in request.form else "",
            "airlaw_attempt4": "✓" if "airlaw_attempt4" in request.form else "",
            "airlaw_date": datetime.datetime.strptime(request.form["airlaw_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("airlaw_date") else "",

            "agk_asp_attempt1": "✓" if "agk_asp_attempt1" in request.form else "",
            "agk_asp_attempt2": "✓" if "agk_asp_attempt2" in request.form else "",
            "agk_asp_attempt3": "✓" if "agk_asp_attempt3" in request.form else "",
            "agk_asp_attempt4": "✓" if "agk_asp_attempt4" in request.form else "",
            "agk_asp_date": datetime.datetime.strptime(request.form["agk_asp_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("agk_asp_date") else "",

            "agk_i_attempt1": "✓" if "agk_i_attempt1" in request.form else "",
            "agk_i_attempt2": "✓" if "agk_i_attempt2" in request.form else "",
            "agk_i_attempt3": "✓" if "agk_i_attempt3" in request.form else "",
            "agk_i_attempt4": "✓" if "agk_i_attempt4" in request.form else "",
            "agk_i_date": datetime.datetime.strptime(request.form["agk_i_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("agk_i_date") else "",

            "mb_attempt1": "✓" if "mb_attempt1" in request.form else "",
            "mb_attempt2": "✓" if "mb_attempt2" in request.form else "",
            "mb_attempt3": "✓" if "mb_attempt3" in request.form else "",
            "mb_attempt4": "✓" if "mb_attempt4" in request.form else "",
            "mb_date": datetime.datetime.strptime(request.form["mb_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("mb_date") else "",

            "perf_attempt1": "✓" if "perf_attempt1" in request.form else "",
            "perf_attempt2": "✓" if "perf_attempt2" in request.form else "",
            "perf_attempt3": "✓" if "perf_attempt3" in request.form else "",
            "perf_attempt4": "✓" if "perf_attempt4" in request.form else "",
            "perf_date": datetime.datetime.strptime(request.form["perf_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("perf_date") else "",

            "fpm_attempt1": "✓" if "fpm_attempt1" in request.form else "",
            "fpm_attempt2": "✓" if "fpm_attempt2" in request.form else "",
            "fpm_attempt3": "✓" if "fpm_attempt3" in request.form else "",
            "fpm_attempt4": "✓" if "fpm_attempt4" in request.form else "",
            "fpm_date": datetime.datetime.strptime(request.form["fpm_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("fpm_date") else "",

            "hpl_attempt1": "✓" if "hpl_attempt1" in request.form else "",
            "hpl_attempt2": "✓" if "hpl_attempt2" in request.form else "",
            "hpl_attempt3": "✓" if "hpl_attempt3" in request.form else "",
            "hpl_attempt4": "✓" if "hpl_attempt4" in request.form else "",
            "hpl_date": datetime.datetime.strptime(request.form["hpl_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("hpl_date") else "",

            "met_attempt1": "✓" if "met_attempt1" in request.form else "",
            "met_attempt2": "✓" if "met_attempt2" in request.form else "",
            "met_attempt3": "✓" if "met_attempt3" in request.form else "",
            "met_attempt4": "✓" if "met_attempt4" in request.form else "",
            "met_date": datetime.datetime.strptime(request.form["met_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("met_date") else "",

            "gnav_attempt1": "✓" if "gnav_attempt1" in request.form else "",
            "gnav_attempt2": "✓" if "gnav_attempt2" in request.form else "",
            "gnav_attempt3": "✓" if "gnav_attempt3" in request.form else "",
            "gnav_attempt4": "✓" if "gnav_attempt4" in request.form else "",
            "gnav_date": datetime.datetime.strptime(request.form["gnav_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("gnav_date") else "",

            "rnav_attempt1": "✓" if "rnav_attempt1" in request.form else "",
            "rnav_attempt2": "✓" if "rnav_attempt2" in request.form else "",
            "rnav_attempt3": "✓" if "rnav_attempt3" in request.form else "",
            "rnav_attempt4": "✓" if "rnav_attempt4" in request.form else "",
            "rnav_date": datetime.datetime.strptime(request.form["rnav_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("rnav_date") else "",

            "ops_attempt1": "✓" if "ops_attempt1" in request.form else "",
            "ops_attempt2": "✓" if "ops_attempt2" in request.form else "",
            "ops_attempt3": "✓" if "ops_attempt3" in request.form else "",
            "ops_attempt4": "✓" if "ops_attempt4" in request.form else "",
            "ops_date": datetime.datetime.strptime(request.form["ops_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("ops_date") else "",

            "pof_attempt1": "✓" if "pof_attempt1" in request.form else "",
            "pof_attempt2": "✓" if "pof_attempt2" in request.form else "",
            "pof_attempt3": "✓" if "pof_attempt3" in request.form else "",
            "pof_attempt4": "✓" if "pof_attempt4" in request.form else "",
            "pof_date": datetime.datetime.strptime(request.form["pof_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("pof_date") else "",

            "comm_attempt1": "✓" if "comm_attempt1" in request.form else "",
            "comm_attempt2": "✓" if "comm_attempt2" in request.form else "",
            "comm_attempt3": "✓" if "comm_attempt3" in request.form else "",
            "comm_attempt4": "✓" if "comm_attempt4" in request.form else "",
            "comm_date": datetime.datetime.strptime(request.form["comm_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("comm_date") else "",

            "declaration_signature": request.form["declaration_signature"],
            "declaration_date": datetime.datetime.now().strftime("%d/%m/%Y"),
        }

        # --- Recalculate Total Exams ---
        subjects = [
            "airlaw", "agk_asp", "agk_i", "mb", "perf",
            "fpm", "hpl", "met", "gnav", "rnav",
            "ops", "pof", "comm"
        ]
        total_exams_count = 0
        for subj in subjects:
            if any(request.form.get(f"{subj}_attempt{i}") for i in range(1, 5)):
                total_exams_count += 1

        if total_exams_count == 0:
            return "Error: You must select at least one subject in Section 4.", 400

        data["total_exams"] = str(total_exams_count)

        # --- Save and Email ---
        filename = f"{data['firstname']}_{data['surname']}_{request.form['class_selection']}_{datetime.datetime.now().strftime('%Y%m%d')}.pdf"
        filepath = os.path.join(OUTPUT_DIR, filename)

        fill_pdf(data, filename)
        send_emails(filepath, data["email"])

        today_str = datetime.datetime.now().strftime("%d/%m/%Y")
        return f"✅ Form submitted successfully on {today_str}. Your HCAA Application has been sent to Global Aviation's team."

    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)

