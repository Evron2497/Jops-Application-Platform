import streamlit as st
import os
import io
from datetime import datetime, date
from fpdf import FPDF

# Page configuration
st.set_page_config(
    page_title="Canada Job Application Portal",
    page_icon="✈️",
    layout="centered"
)

# Custom App Styling
st.markdown("""
    <style>
    .main-header {
        font-size: 28px;
        font-weight: bold;
        color: #C51A1B;
        text-align: center;
        margin-bottom: 20px;
    }
    .section-head {
        font-size: 20px;
        font-weight: bold;
        color: #1E3A8A;
        border-bottom: 2px solid #1E3A8A;
        padding-bottom: 5px;
        margin-top: 25px;
        margin-bottom: 15px;
    }
    .promo-box {
        background-color: #F8FAFC;
        border-left: 5px solid #C51A1B;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# Application Header & Info Panel
st.markdown("<div class='main-header'>✈️ WORK IN CANADA – VISA & AIR TICKET SPONSORED</div>", unsafe_allow_html=True)

st.markdown("""
<div class='promo-box'>
    <strong>Sponsorship Program Details:</strong><br>
    We’re helping qualified individuals secure jobs in Canada with visa and air ticket fully sponsored by the employer. 
    You only pay <strong>Ksh 25,000</strong> once for processing.
</div>
""", unsafe_allow_html=True)

st.write("Please fill out the form below accurately. All sections must be completed as required.")

# Create a form container
with st.form(key="canada_application_form", clear_on_submit=False):

    # --- Section 1: Personal Information ---
    st.markdown("<div class='section-head'>Section 1: Personal Information</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        full_name = st.text_input("Full Name (as shown on passport)*")
        dob = st.date_input("Date of Birth*", min_value=date(1950, 1, 1), max_value=date.today())
        national_id = st.text_input("National ID Number*")
        marital_status = st.selectbox("Marital Status*", ["Single", "Married", "Divorced", "Widowed"])
    with col2:
        gender = st.selectbox("Gender*", ["Male", "Female", "Other"])
        nationality = st.text_input("Nationality*", value="Kenyan")
        passport_no = st.text_input("Passport Number (if available)")
        passport_expiry = st.date_input("Passport Expiry Date (if applicable)", min_value=date.today())

    county = st.text_input("County of Residence*")
    physical_address = st.text_area("Current Physical Address*", height=100)

    # --- Section 2: Contact Information ---
    st.markdown("<div class='section-head'>Section 2: Contact Information</div>", unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    with col3:
        phone_whatsapp = st.text_input("Phone Number (WhatsApp)*", placeholder="e.g., +254...")
        email = st.text_input("Email Address*")
    with col4:
        phone_alt = st.text_input("Alternative Phone Number")

    # --- Section 3: Education ---
    st.markdown("<div class='section-head'>Section 3: Education</div>", unsafe_allow_html=True)
    
    col5, col6 = st.columns(2)
    with col5:
        edu_level = st.selectbox("Highest Level of Education*", ["High School", "Certificate", "Diploma", "Bachelor's Degree", "Master's Degree", "PhD"])
        course = st.text_input("Course Studied*")
    with col6:
        institution = st.text_input("College/University*")
        year_completed = st.text_input("Year Completed*", max_chars=4)

    # --- Section 4: Work Experience ---
    st.markdown("<div class='section-head'>Section 4: Work Experience</div>", unsafe_allow_html=True)
    
    col7, col8 = st.columns(2)
    with col7:
        current_occupation = st.text_input("Current Occupation*")
        years_exp = st.number_input("Years of Experience*", min_value=0, step=1)
    with col8:
        employer = st.text_input("Current/Last Employer*")
        
    prev_history = st.text_area("Previous Employment History (Roles & Companies)*")
    skills = st.text_area("Skills and Qualifications*")

    # --- Section 5: Canada Job Preferences ---
    st.markdown("<div class='section-head'>Section 5: Canada Job Preferences</div>", unsafe_allow_html=True)
    
    job_categories = ["Housekeeper", "Warehouse Keeper", "Warehouse Clerk", "Airport Cleaner", "Sales Promoter", "Sales Writer", "Receptionist", "Security", "Caregiver", "Drivers", "Nurses", "Supermarket Attendants", "Hostess", "Agriculture", "Dairy Farming", "Construction", "Hospitality", "Cleaning", "Factory Worker", "Other"]
    preferred_category = st.selectbox("Preferred Job Category*", job_categories)
    
    provinces = ["Any Province", "Ontario", "Alberta", "British Columbia", "Manitoba", "Saskatchewan"]
    preferred_province = st.selectbox("Preferred Province*", provinces)
    
    expected_salary = st.text_input("Expected Salary (Optional)")

    # --- Section 6: Language ---
    st.markdown("<div class='section-head'>Section 6: Language</div>", unsafe_allow_html=True)
    
    english_comm = st.radio("Can you communicate in English?*", ["Yes", "No"])
    ielts_score = st.text_input("IELTS or CELPIP Score (if available)")

    # --- Section 7: Travel History ---
    st.markdown("<div class='section-head'>Section 7: Travel History</div>", unsafe_allow_html=True)
    
    travel_outside_ke = st.radio("Have you ever travelled outside Kenya?*", ["No", "Yes"])
    visa_denied = st.radio("Have you ever been denied a visa?*", ["No", "Yes"])
    visa_denied_reason = st.text_area("If yes to visa denial, please explain:")

    # --- Section 8: Document Upload ---
    st.markdown("<div class='section-head'>Section 8: Document Upload</div>", unsafe_allow_html=True)
    st.caption("Allowed file types: PDF, PNG, JPG, JPEG")
    
    u_passport = st.file_uploader("Upload Passport", type=['pdf', 'jpg', 'jpeg', 'png'])
    u_id = st.file_uploader("Upload National ID*", type=['pdf', 'jpg', 'jpeg', 'png'])
    u_cv = st.file_uploader("Upload CV/Resume*", type=['pdf', 'docx'])
    u_certs = st.file_uploader("Upload Academic Certificates*", type=['pdf'])
    u_photo = st.file_uploader("Upload Passport-size Photo*", type=['jpg', 'jpeg', 'png'])
    u_prof_certs = st.file_uploader("Upload Any Professional Certificates (Optional)", type=['pdf'])

    # Submission button
    submit_button = st.form_submit_button(label="Submit Application")

# Clean inputs to prevent encoding failures
def clean_txt(val):
    if not val:
        return ""
    mapping = {
        chr(8216): "'", chr(8217): "'", chr(8218): "'", chr(8219): "'",
        chr(8220): '"', chr(8221): '"', chr(8211): "-", chr(8212): "-",
        "’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-"
    }
    cleaned = str(val)
    for k, v in mapping.items():
        cleaned = cleaned.replace(k, v)
    return cleaned.encode('ascii', errors='ignore').decode('ascii')

# Post-submit handling
if submit_button:
    if not full_name or not national_id or not phone_whatsapp or not email:
        st.error("Please fill in all mandatory fields (marked with *) before submitting.")
    elif not u_id or not u_cv or not u_certs or not u_photo:
        st.error("Please upload all mandatory documents (National ID, CV, Academic Certificates, and Passport-size Photo).")
    else:
        st.success("Your online application form details have been successfully captured!")
        
        try:
            pdf = FPDF(orientation="P", unit="mm", format="A4")
            pdf.set_margin(15)
            
            # --- PAGE 1: CONDITIONAL LETTER OF INTENT ---
            pdf.add_page()
            pdf.set_fill_color(197, 26, 27)
            pdf.rect(15, 15, 180, 2, 'F')
            
            pdf.ln(5)
            pdf.set_font("Arial", "B", 18)
            pdf.set_text_color(197, 26, 27)
            pdf.cell(0, 10, "CANADA GLOBAL RECRUITMENT PATHWAYS", ln=True)
            
            pdf.set_font("Arial", "B", 11)
            pdf.set_text_color(30, 58, 138)
            pdf.cell(0, 5, "Official Conditional Assessment & Intake Letter", ln=True)
            
            pdf.set_font("Arial", "", 9)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 5, f"Date: {datetime.today().strftime('%B %d, %Y')}", ln=True)
            
            # Embed Passport Photo inside header structure
            if u_photo is not None:
                try:
                    photo_bytes = io.BytesIO(u_photo.read())
                    u_photo.seek(0)
                    pdf.image(photo_bytes, x=155, y=23, w=35, h=40)
                except Exception:
                    pass
            
            pdf.ln(15)
            
            # Client info grid layout
            pdf.set_fill_color(248, 250, 252)
            pdf.set_draw_color(226, 232, 240)
            pdf.rect(15, 52, 135, 32, 'DF')
            
            pdf.set_text_color(30, 58, 138)
            pdf.set_font("Arial", "B", 10)
            
            pdf.set_xy(17, 54)
            pdf.cell(30, 5, "Applicant:")
            pdf.set_font("Arial", "", 10)
            pdf.set_text_color(50, 50, 50)
            pdf.cell(45, 5, clean_txt(full_name))
            
            pdf.set_font("Arial", "B", 10)
            pdf.set_text_color(30, 58, 138)
            pdf.cell(25, 5, "National ID:")
            pdf.set_font("Arial", "", 10)
            pdf.set_text_color(50, 50, 50)
            pdf.cell(30, 5, clean_txt(national_id), ln=True)
            
            pdf.set_xy(17, 62)
            pdf.set_font("Arial", "B", 10)
            pdf.set_text_color(30, 58, 138)
            pdf.cell(30, 5, "Pref. Job:")
            pdf.set_font("Arial", "", 10)
            pdf.set_text_color(50, 50, 50)
            pdf.cell(45, 5, clean_txt(preferred_category))
            
            pdf.set_font("Arial", "B", 10)
            pdf.set_text_color(30, 58, 138)
            pdf.cell(25, 5, "Province:")
            pdf.set_font("Arial", "", 10)
            pdf.set_text_color(50, 50, 50)
            pdf.cell(30, 5, clean_txt(preferred_province), ln=True)

            pdf.set_xy(17, 70)
            pdf.set_font("Arial", "B", 10)
            pdf.set_text_color(30, 58, 138)
            pdf.cell(30, 5, "Email:")
            pdf.set_font("Arial", "", 9)
            pdf.set_text_color(50, 50, 50)
            pdf.cell(45, 5, clean_txt(email))
            
            pdf.set_font("Arial", "B", 10)
            pdf.set_text_color(30, 58, 138)
            pdf.cell(25, 5, "WhatsApp:")
            pdf.set_font("Arial", "", 10)
            pdf.set_text_color(50, 50, 50)
            pdf.cell(30, 5, clean_txt(phone_whatsapp), ln=True)
            
            pdf.set_xy(15, 90)
            pdf.set_font("Arial", "", 10)
            pdf.set_text_color(33, 33, 33)
            
            letter_text = (
                "Hello,\n\n"
                "My name is Joyce K, a registered nurse and a Kenyan citizen currently working in Canada. "
                "I hope you're doing well.\n\n"
                "I'm reaching out to kindly share an opportunity that may be of interest to you. At the moment, "
                "there are job openings here in Canada across various sectors, and I would like to know if you might "
                "be interested in working here as well.\n\n"
                "The positions available are legitimate and supported by employers who offer visa and air ticket "
                "sponsorship. In most cases, accommodation is also provided for the first few months to help you "
                "settle in smoothly.\n\n"
                "If you're seriously considering this opportunity, I'd be happy to guide you through the process, "
                "explain the requirements, and answer any questions you may have. Please feel free to let me know "
                "if you're interested or would like more information. I'll be glad to assist you step by step.\n\n"
                "CURRENT DEMAND SECTORS & OPEN POSITIONS IN CANADA:\n"
                " - Housekeeper            - Warehouse Keeper         - Warehouse Clerk\n"
                " - Airport Cleaner         - Sales Promoter             - Sales Writer\n"
                " - Receptionist             - Security Officer             - Caregiver / CNA\n"
                " - Commercial Drivers    - Registered Nurses          - Supermarket Attendants\n"
                " - Corporate Hostess      - Agriculture Worker         - Dairy Farmer\n"
            )
            pdf.multi_cell(0, 5, clean_txt(letter_text))
            
            pdf.ln(2)
            current_y = pdf.get_y()
            pdf.set_fill_color(255, 245, 245)
            pdf.set_draw_color(197, 26, 27)
            pdf.rect(15, current_y, 180, 24, 'DF')
            
            pdf.set_xy(18, current_y + 2)
            pdf.set_font("Arial", "B", 10)
            pdf.set_text_color(197, 26, 27)
            pdf.cell(0, 5, "MANDATORY WORK PERMIT PROCESSING FEE REQUIREMENT", ln=True)
            
            pdf.set_xy(18, current_y + 8)
            pdf.set_font("Arial", "", 9)
            pdf.set_text_color(50, 50, 50)
            warning_msg = (
                "Your digital files have been checked against initial screening metrics. To officially submit your profile "
                "to our employment pool and kickstart your work permit acquisition, a fixed processing fee of Ksh 25,000 "
                "is required. This safe transaction covers mandatory administrative evaluations and ensures documentation alignment."
            )
            pdf.multi_cell(174, 4, clean_txt(warning_msg))
            
            pdf.set_xy(15, current_y + 28)
            pdf.set_font("Arial", "", 10)
            pdf.set_text_color(33, 33, 33)
            pdf.multi_cell(0, 5, clean_txt("Please save this conditional intake document securely. Our appointed verification desk agent will get in touch using your registered contact details shortly to complete file verification."))
            
            pdf.ln(5)
            pdf.set_font("Arial", "I", 10)
            pdf.cell(0, 5, "Digitally Signed & Certified", ln=True)
            pdf.set_font("Arial", "B", 10)
            pdf.cell(0, 5, "Joyce K.", ln=True)
            pdf.set_font("Arial", "", 9)
            pdf.cell(0, 4, "Registered Nurse & Recruitment Liaison", ln=True)
            pdf.cell(0, 4, "Ontario, Canada", ln=True)
            
            # --- PAGE 2: CAPTURED DATA AUDIT REPORT ---
            pdf.add_page()
            pdf.set_fill_color(30, 58, 138)
            pdf.rect(15, 15, 180, 2, 'F')
            
            pdf.ln(5)
            pdf.set_font("Arial", "B", 14)
            pdf.set_text_color(30, 58, 138)
            pdf.cell(0, 8, "APPENDIX A: SYSTEM CAPTURED DATA RECORD", ln=True)
            pdf.set_font("Arial", "", 9)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 4, "The following structured breakdown constitutes your digital file manifest captured by the portal log.", ln=True)
            pdf.ln(6)
            
            def draw_row(label, val):
                pdf.set_font("Arial", "B", 10)
                pdf.set_text_color(30, 58, 138)
                pdf.cell(50, 6, clean_txt(label), border=1)
                pdf.set_font("Arial", "", 10)
                pdf.set_text_color(50, 50, 50)
                pdf.cell(130, 6, clean_txt(val), border=1, ln=True)

            draw_row("Full Passport Name", full_name)
            draw_row("Date of Birth", str(dob))
            draw_row("National Identification No", national_id)
            draw_row("Marital Status", marital_status)
            draw_row("Gender / Nationality", f"{gender} / {nationality}")
            draw_row("Passport No / Expiry", f"{passport_no if passport_no else 'N/A'} (Exp: {passport_expiry})")
            draw_row("County of Residence", county)
            draw_row("Physical Location", physical_address.replace('\n', ' '))
            draw_row("WhatsApp Mobile Line", phone_whatsapp)
            draw_row("Secondary Contact Line", phone_alt if phone_alt else "N/A")
            draw_row("Email Profile Address", email)
            draw_row("Education Level Attained", edu_level)
            draw_row("Specialized Course Field", course)
            draw_row("Institution / University", institution)
            draw_row("Graduation Calendar Year", year_completed)
            draw_row("Current Designated Role", current_occupation)
            draw_row("Verified Working Experience", f"{years_exp} Years")
            draw_row("Last Registered Employer", employer)
            draw_row("Target Employment Sector", preferred_category)
            draw_row("Destination Province", preferred_province)
            draw_row("Expected Wage / Remuneration", expected_salary if expected_salary else "Employer Discretion")
            draw_row("English Competency / IELTS", f"Can Speak: {english_comm} (IELTS: {ielts_score if ielts_score else 'None'})")
            draw_row("International Travel Status", f"Traveled: {travel_outside_ke} | Denied Visa: {visa_denied}")
            
            if visa_denied == "Yes":
                draw_row("Visa Interdiction Basis", visa_denied_reason.replace('\n', ' '))
                
            pdf.ln(10)
            pdf.set_font("Arial", "B", 10)
            pdf.set_text_color(197, 26, 27)
            pdf.cell(0, 5, "UPLOADED CREDENTIAL CHECKLIST MANIFEST:", ln=True)
            
            pdf.set_font("Arial", "", 9.5)
            pdf.set_text_color(50, 50, 50)
            pdf.cell(0, 5, f"[X] Passport Document Attachment: {u_passport.name if u_passport else 'Not Provided'}", ln=True)
            pdf.cell(0, 5, f"[X] Government National ID Card: {u_id.name}", ln=True)
            pdf.cell(0, 5, f"[X] Professional CV / Chronological Resume: {u_cv.name}", ln=True)
            pdf.cell(0, 5, f"[X] Scholastic Academic Certificates: {u_certs.name}", ln=True)
            pdf.cell(0, 5, f"[X] Biometric Passport-Size Portrait: {u_photo.name}", ln=True)
            pdf.cell(0, 5, f"[X] Professional Credentials (Optional): {u_prof_certs.name if u_prof_certs else 'Not Provided'}", ln=True)

            # --- SYSTEM COMPILING REPAIR ---
            pdf_buffer = io.BytesIO()
            pdf.output(pdf_buffer)
            pdf_bytes = pdf_buffer.getvalue()
            
            st.markdown("### 📄 Your Application Package is Ready")
            st.info("The system has assembled your official application packet. Use the download trigger below to pull your verified letter and audit receipt.")
            
            st.download_button(
                label="⬇️ Download Official Canada Intake Package (PDF)",
                data=pdf_bytes,
                file_name=f"Canada_Application_Package_{full_name.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
            
        except Exception as pdf_error:
            st.error(f"Error compiling document: {str(pdf_error)}")

# WhatsApp Instructions Panel
# WhatsApp Instructions Panel
st.markdown("""
---
### 📲 Next Step: Complete Your Submission via WhatsApp
To complete your verification and begin processing your application, you **must** send the downloaded document or your primary details directly to our recruitment team. 

Click the button below to automatically open our official WhatsApp desk:
""", unsafe_allow_html=True)

# --- CUSTOM WHATSAPP DIRECTION LINK ---
# Replace the phone number below with your actual phone number including country code (e.g., 254712345678)
# Do NOT include spaces, dashes, or a leading '+' sign.
whatsapp_phone = "254769065385"  
whatsapp_message = "Hello, I have completed my Canada Application form online. Here is my package."

# URL-encoded text link
encoded_msg = whatsapp_message.replace(" ", "%20")
whatsapp_url = f"https://wa.me/{whatsapp_phone}?text={encoded_msg}"

# CSS Styled clickable button with an icon
st.markdown(f"""
    <a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">
        <div style="
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background-color: #25D366;
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 16px;
            font-family: Arial, sans-serif;
            box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
            cursor: pointer;
            transition: 0.3s;">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-whatsapp" viewBox="0 0 16 16" style="margin-right: 10px;">
                <path d="M13.601 2.326A7.85 7.85 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.9 7.9 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.9 7.9 0 0 0 13.6 2.326zM7.994 14.521a6.6 6.6 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.56 6.56 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592m3.69-4.294c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.73.73 0 0 0-.529.247c-.182.198-.691.677-.691 1.654s.71 1.916.81 2.049c.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232"/>
            </svg>
            Chat with Verification Desk
        </div>
    </a>
""", unsafe_allow_html=True)

st.markdown("""
<br>
<ul>
    <li>🪪 <b>Clear photo of your National ID</b> (front & back)</li>
    <li>📸 <b>Passport-size photo</b></li>
    <li>📧 <b>Your active email address</b></li>
    <li>🧍‍♂️ <b>Your full name</b></li>
    <li>📍 <b>Your current location</b></li>
</ul>
<p><i>Ensure you have the Ksh 25,000 processing fee ready when contacted by our verification agent.</i></p>
""", unsafe_allow_html=True)