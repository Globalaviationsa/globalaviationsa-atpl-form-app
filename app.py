from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfReader, PdfWriter
import os, datetime, smtplib
from email.message import EmailMessage

app = Flask(__name__)

# Your pre-filled template PDF (must be in the same folder as this app.py)
TEMPLATE_PDF = "ATPL_Class_Spring2025_Template.pdf"
OUTPUT_DIR = "filled_pdfs"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- PDF FILL FUNCTION ---
def fill_pdf(student_data, output_filename):
    overlay_path = "overlay.pdf"
    c = canvas.Canvas(overlay_path, pagesize=A4)
   
    # --- Personal Details (Section 1) ---
    c.setFont("Helvetica-Bold", 10)  # bold + slightly larger
    c.drawString(75, 608, student_data["surname"].upper())        # Surname
    c.drawString(350, 608, student_data["firstname"].upper())      # First Name(s)
    c.drawString(125, 588.5, student_data["title"].upper())          # Title (Mr/Ms/etc.)
    c.drawString(405, 588.5, student_data["dob"].upper())            # Date of Birth
    c.drawString(78, 570, student_data["nationality"].upper())    # Nationality
    c.drawString(380, 570, student_data["birthplace_town"].upper())     # Place of Birth (Town)
    c.drawString(488, 570, student_data["birthplace_country"].upper())     # Place of Birth (Country)
    c.drawString(120, 550, student_data["address"].upper())        # Permanent Address
    c.drawString(335, 531, student_data["postcode"].upper())       # Postcode
    c.drawString(100, 511, student_data["phone"].upper())          # Contact Tel. No.
    c.drawString(358, 511, student_data["mobile"].upper())         # Mobile Tel. No.
    c.drawString(100, 492, student_data["email"])          # E-mail Address
    
    # --- Page 2 : Switch to new page ---
    c.showPage()

    # --- Page 2 : Air Law row ---
    c.setFont("Helvetica-Bold", 10)
    c.drawString(345, 646, student_data["airlaw_attempt1"])   # Attempt 1
    c.drawString(382, 646, student_data["airlaw_attempt2"])   # Attempt 2
    c.drawString(418, 646, student_data["airlaw_attempt3"])   # Attempt 3
    c.drawString(453, 646, student_data["airlaw_attempt4"])   # Attempt 4
    c.drawString(480, 646, student_data["airlaw_date"])       # Date Passed

    # --- Page 2 : Aircraft General Knowledge_Airframe/Systems/Powerplant row ---
    c.setFont("Helvetica-Bold", 10)
    c.drawString(345, 630, student_data["agk_asp_attempt1"])   # Attempt 1
    c.drawString(382, 630, student_data["agk_asp_attempt2"])   # Attempt 2
    c.drawString(418, 630, student_data["agk_asp_attempt3"])   # Attempt 3
    c.drawString(453, 630, student_data["agk_asp_attempt4"])   # Attempt 4
    c.drawString(480, 630, student_data["agk_asp_date"])       # Date Passed

    # --- Page 2 : Aircraft General Knowledge_Instrumentation row ---
    c.setFont("Helvetica-Bold", 10)
    c.drawString(345, 614, student_data["agk_i_attempt1"])   # Attempt 1
    c.drawString(382, 614, student_data["agk_i_attempt2"])   # Attempt 2
    c.drawString(418, 614, student_data["agk_i_attempt3"])   # Attempt 3
    c.drawString(453, 614, student_data["agk_i_attempt4"])   # Attempt 4
    c.drawString(480, 614, student_data["agk_i_date"])       # Date Passed

    # --- Page 2 : Mass and Balance row ---
    c.setFont("Helvetica-Bold", 10)
    c.drawString(345, 597, student_data["mb_attempt1"])   # Attempt 1
    c.drawString(382, 597, student_data["mb_attempt2"])   # Attempt 2
    c.drawString(418, 597, student_data["mb_attempt3"])   # Attempt 3
    c.drawString(453, 597, student_data["mb_attempt4"])   # Attempt 4
    c.drawString(480, 597, student_data["mb_date"])       # Date Passed    

    # --- Page 2 : Performance row ---
    c.setFont("Helvetica-Bold", 10)
    c.drawString(345, 581, student_data["perf_attempt1"])   # Attempt 1
    c.drawString(382, 581, student_data["perf_attempt2"])   # Attempt 2
    c.drawString(418, 581, student_data["perf_attempt3"])   # Attempt 3
    c.drawString(453, 581, student_data["perf_attempt4"])   # Attempt 4
    c.drawString(480, 581, student_data["perf_date"])       # Date Passed

    # --- Page 2 : Flight Planning and Monitoring row ---
    c.setFont("Helvetica-Bold", 10)
    c.drawString(345, 565, student_data["fpm_attempt1"])   # Attempt 1
    c.drawString(382, 565, student_data["fpm_attempt2"])   # Attempt 2
    c.drawString(418, 565, student_data["fpm_attempt3"])   # Attempt 3
    c.drawString(453, 565, student_data["fpm_attempt4"])   # Attempt 4
    c.drawString(480, 565, student_data["fpm_date"])       # Date Passed

    # --- Page 2 : Human Performance and Limitations row ---
    c.setFont("Helvetica-Bold", 10)
    c.drawString(345, 548, student_data["hpl_attempt1"])   # Attempt 1
    c.drawString(382, 548, student_data["hpl_attempt2"])   # Attempt 2
    c.drawString(418, 548, student_data["hpl_attempt3"])   # Attempt 3
    c.drawString(453, 548, student_data["hpl_attempt4"])   # Attempt 4
    c.drawString(480, 548, student_data["hpl_date"])       # Date Passed

    # --- Page 2 : Meteorology row ---
    c.setFont("Helvetica-Bold", 10)
    c.drawString(345, 532, student_data["met_attempt1"])   # Attempt 1
    c.drawString(382, 532, student_data["met_attempt2"])   # Attempt 2
    c.drawString(418, 532, student_data["met_attempt3"])   # Attempt 3
    c.drawString(453, 532, student_data["met_attempt4"])   # Attempt 4
    c.drawString(480, 532, student_data["met_date"])       # Date Passed

    # --- Page 2 : General Navigation row ---
    c.setFont("Helvetica-Bold", 10)
    c.drawString(345, 516, student_data["gnav_attempt1"])   # Attempt 1
    c.drawString(382, 516, student_data["gnav_attempt2"])   # Attempt 2
    c.drawString(418, 516, student_data["gnav_attempt3"])   # Attempt 3
    c.drawString(453, 516, student_data["gnav_attempt4"])   # Attempt 4
    c.drawString(480, 516, student_data["gnav_date"])       # Date Passed

    # --- Page 2 : Radio Navigation row ---
    c.setFont("Helvetica-Bold", 10)
    c.drawString(345, 500, student_data["rnav_attempt1"])   # Attempt 1
    c.drawString(382, 500, student_data["rnav_attempt2"])   # Attempt 2
    c.drawString(418, 500, student_data["rnav_attempt3"])   # Attempt 3
    c.drawString(453, 500, student_data["rnav_attempt4"])   # Attempt 4
    c.drawString(480, 500, student_data["rnav_date"])       # Date Passed    

    # --- Page 2 : Operational Procedures row ---
    c.setFont("Helvetica-Bold", 10)
    c.drawString(345, 484, student_data["ops_attempt1"])   # Attempt 1
    c.drawString(382, 484, student_data["ops_attempt2"])   # Attempt 2
    c.drawString(418, 484, student_data["ops_attempt3"])   # Attempt 3
    c.drawString(453, 484, student_data["ops_attempt4"])   # Attempt 4
    c.drawString(480, 484, student_data["ops_date"])       # Date Passed

    # --- Page 2 : Principles of Flight row ---
    c.setFont("Helvetica-Bold", 10)
    c.drawString(345, 468, student_data["pof_attempt1"])   # Attempt 1
    c.drawString(382, 468, student_data["pof_attempt2"])   # Attempt 2
    c.drawString(418, 468, student_data["pof_attempt3"])   # Attempt 3
    c.drawString(453, 468, student_data["pof_attempt4"])   # Attempt 4
    c.drawString(480, 468, student_data["pof_date"])       # Date Passed

    # --- Page 2 : Communications row ---
    c.setFont("Helvetica-Bold", 10)
    c.drawString(345, 452, student_data["comm_attempt1"])   # Attempt 1
    c.drawString(382, 452, student_data["comm_attempt2"])   # Attempt 2
    c.drawString(418, 452, student_data["comm_attempt3"])   # Attempt 3
    c.drawString(453, 452, student_data["comm_attempt4"])   # Attempt 4
    c.drawString(480, 452, student_data["comm_date"])       # Date Passed
    
    # --- Page 2 : Total Exams ---
    c.setFont("Helvetica-Bold", 10)
    c.drawString(345, 436, student_data["total_exams"])

    # --- PAGE 3 : Declaration ---
    c.showPage()
    c.setFont("Helvetica-Bold", 11)

    # Signature
    c.drawString(70, 421, student_data["declaration_signature"].upper())

    # Date
    c.drawString(315, 421, student_data["declaration_date"])

    c.save()

    # --- MERGE WITH TEMPLATE ---
    template = PdfReader(open(TEMPLATE_PDF, "rb"))
    overlay = PdfReader(open(overlay_path, "rb"))
    writer = PdfWriter()

    # Merge overlay page by page
    for i, page in enumerate(template.pages):
        if i < len(overlay.pages):
            page.merge_page(overlay.pages[i])
        writer.add_page(page)

    with open(os.path.join(OUTPUT_DIR, output_filename), "wb") as f:
        writer.write(f)

# --- HELPER FUNCTION TO EMAIL PDFs ---
def send_pdf_via_email(pdf_path):
    try:
        print("📧 Preparing email...")

        msg = EmailMessage()
        msg["Subject"] = "New ATPL Application Form Submission"
        msg["From"] = os.environ["EMAIL_USER"]
        msg["To"] = os.environ["EMAIL_USER"]
        msg.set_content("Attached is a completed ATPL application form.")

        with open(pdf_path, "rb") as f:
            file_data = f.read()
            msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=os.path.basename(pdf_path))

        print("📡 Connecting to SMTP...")
        with smtplib.SMTP("mail.globalaviationsa.com", 587) as smtp:
            smtp.starttls()
            smtp.login(os.environ["EMAIL_USER"], os.environ["EMAIL_PASS"])
            smtp.send_message(msg)

        print("✅ Email sent successfully!")
    except Exception as e:
        print("❌ Error sending email:", e)

# --- WEB ROUTE ---
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
# --- REQUIRED FIELD VALIDATION ---
        if not request.form["surname"] or not request.form["firstname"] or not request.form["title"] or not request.form["dob"] or not request.form["nationality"] or not request.form["birthplace_town"] or not request.form["birthplace_country"] or not request.form["address"] or not request.form["postcode"] or not request.form["phone"] or not request.form["mobile"] or not request.form["email"] or not request.form["declaration_signature"] or not request.form["declaration_date"]:
            return "Error: You must fill all required fields in Section 1 Personal Details as well as Section 7 Declaration", 400
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
        
	    # --- Air Law Section ---
	    "airlaw_attempt1": "✓" if "airlaw_attempt1" in request.form else "",
	    "airlaw_attempt2": "✓" if "airlaw_attempt2" in request.form else "",
	    "airlaw_attempt3": "✓" if "airlaw_attempt3" in request.form else "",
	    "airlaw_attempt4": "✓" if "airlaw_attempt4" in request.form else "",
	    "airlaw_date": datetime.datetime.strptime(request.form["airlaw_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("airlaw_date") else "",

	    # --- Aircraft General Knowledge_Airframe/Systems/Powerplant Section ---
	    "agk_asp_attempt1": "✓" if "agk_asp_attempt1" in request.form else "",
	    "agk_asp_attempt2": "✓" if "agk_asp_attempt2" in request.form else "",
	    "agk_asp_attempt3": "✓" if "agk_asp_attempt3" in request.form else "",
	    "agk_asp_attempt4": "✓" if "agk_asp_attempt4" in request.form else "",
	    "agk_asp_date": datetime.datetime.strptime(request.form["agk_asp_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("agk_asp_date") else "",

	    # --- Aircraft General Knowledge_Instrumentation Section ---
	    "agk_i_attempt1": "✓" if "agk_i_attempt1" in request.form else "",
	    "agk_i_attempt2": "✓" if "agk_i_attempt2" in request.form else "",
	    "agk_i_attempt3": "✓" if "agk_i_attempt3" in request.form else "",
	    "agk_i_attempt4": "✓" if "agk_i_attempt4" in request.form else "",
	    "agk_i_date": datetime.datetime.strptime(request.form["agk_i_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("agk_i_date") else "",

	    # --- Mass and Balance Section ---
	    "mb_attempt1": "✓" if "mb_attempt1" in request.form else "",
	    "mb_attempt2": "✓" if "mb_attempt2" in request.form else "",
	    "mb_attempt3": "✓" if "mb_attempt3" in request.form else "",
	    "mb_attempt4": "✓" if "mb_attempt4" in request.form else "",
	    "mb_date": datetime.datetime.strptime(request.form["mb_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("mb_date") else "",

	    # --- Performance Section ---
	    "perf_attempt1": "✓" if "perf_attempt1" in request.form else "",
	    "perf_attempt2": "✓" if "perf_attempt2" in request.form else "",
	    "perf_attempt3": "✓" if "perf_attempt3" in request.form else "",
	    "perf_attempt4": "✓" if "perf_attempt4" in request.form else "",
	    "perf_date": datetime.datetime.strptime(request.form["perf_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("perf_date") else "",

	    # --- Flight Planning and Monitoring Section ---
	    "fpm_attempt1": "✓" if "fpm_attempt1" in request.form else "",
	    "fpm_attempt2": "✓" if "fpm_attempt2" in request.form else "",
	    "fpm_attempt3": "✓" if "fpm_attempt3" in request.form else "",
	    "fpm_attempt4": "✓" if "fpm_attempt4" in request.form else "",
	    "fpm_date": datetime.datetime.strptime(request.form["fpm_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("fpm_date") else "",

	    # --- Human Performance and Limitations Section ---
	    "hpl_attempt1": "✓" if "hpl_attempt1" in request.form else "",
	    "hpl_attempt2": "✓" if "hpl_attempt2" in request.form else "",
	    "hpl_attempt3": "✓" if "hpl_attempt3" in request.form else "",
	    "hpl_attempt4": "✓" if "hpl_attempt4" in request.form else "",
	    "hpl_date": datetime.datetime.strptime(request.form["hpl_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("hpl_date") else "",

	    # --- Meteorology Section ---
	    "met_attempt1": "✓" if "met_attempt1" in request.form else "",
	    "met_attempt2": "✓" if "met_attempt2" in request.form else "",
	    "met_attempt3": "✓" if "met_attempt3" in request.form else "",
	    "met_attempt4": "✓" if "met_attempt4" in request.form else "",
	    "met_date": datetime.datetime.strptime(request.form["met_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("met_date") else "",

	    # --- General Navigation Section ---
	    "gnav_attempt1": "✓" if "gnav_attempt1" in request.form else "",
	    "gnav_attempt2": "✓" if "gnav_attempt2" in request.form else "",
	    "gnav_attempt3": "✓" if "gnav_attempt3" in request.form else "",
	    "gnav_attempt4": "✓" if "gnav_attempt4" in request.form else "",
	    "gnav_date": datetime.datetime.strptime(request.form["gnav_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("gnav_date") else "",

	    # --- Radio Navigation Section ---
	    "rnav_attempt1": "✓" if "rnav_attempt1" in request.form else "",
	    "rnav_attempt2": "✓" if "rnav_attempt2" in request.form else "",
	    "rnav_attempt3": "✓" if "rnav_attempt3" in request.form else "",
	    "rnav_attempt4": "✓" if "rnav_attempt4" in request.form else "",
	    "rnav_date": datetime.datetime.strptime(request.form["rnav_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("rnav_date") else "",

	    # --- Operational Procedures Section ---
	    "ops_attempt1": "✓" if "ops_attempt1" in request.form else "",
	    "ops_attempt2": "✓" if "ops_attempt2" in request.form else "",
	    "ops_attempt3": "✓" if "ops_attempt3" in request.form else "",
	    "ops_attempt4": "✓" if "ops_attempt4" in request.form else "",
	    "ops_date": datetime.datetime.strptime(request.form["ops_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("ops_date") else "",

	     # --- Principles of Flight Section ---
	    "pof_attempt1": "✓" if "pof_attempt1" in request.form else "",
	    "pof_attempt2": "✓" if "pof_attempt2" in request.form else "",
	    "pof_attempt3": "✓" if "pof_attempt3" in request.form else "",
	    "pof_attempt4": "✓" if "pof_attempt4" in request.form else "",
	    "pof_date": datetime.datetime.strptime(request.form["pof_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("pof_date") else "",

	     # --- Communications Section ---
	    "comm_attempt1": "✓" if "comm_attempt1" in request.form else "",
	    "comm_attempt2": "✓" if "comm_attempt2" in request.form else "",
	    "comm_attempt3": "✓" if "comm_attempt3" in request.form else "",
	    "comm_attempt4": "✓" if "comm_attempt4" in request.form else "",
	    "comm_date": datetime.datetime.strptime(request.form["comm_date"], "%Y-%m-%d").strftime("%d/%m/%Y") if request.form.get("comm_date") else "",

	    "declaration_signature": request.form["declaration_signature"],
	    "declaration_date": datetime.datetime.now().strftime("%d/%m/%Y"),

	}

        # --- Recalculate Total Exams on the server side ---
        subjects = [
            "airlaw", "agk_asp", "agk_i", "mb", "perf",
            "fpm", "hpl", "met", "gnav", "rnav",
            "ops", "pof", "comm"
        ]

        total_exams_count = 0
        for subj in subjects:
            if any(request.form.get(f"{subj}_attempt{i}") for i in range(1, 5)):
                total_exams_count += 1

        # ✅ Block submission if no subjects selected
        if total_exams_count == 0:
            return "Error: You must select at least one subject in Section 4.", 400

        data["total_exams"] = str(total_exams_count)

        # Save with unique filename (Surname + timestamp)
        filename = f"{data['surname']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(OUTPUT_DIR, filename)

        fill_pdf(data, filename)

        # ✅ Only ONE call here
        send_pdf_via_email(filepath)

        today_str = datetime.datetime.now().strftime("%d/%m/%Y")
        return f"✅ Form submitted successfully on {today_str}. The PDF has been sent to the administrator."

    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)
