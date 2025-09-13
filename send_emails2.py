import os
import smtplib
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
from email.utils import formataddr

# --- IMPORTANT: Import your secret credentials ---
try:
    import config
except ImportError:
    print("❌ Error: config.py not found. Please create it and add your EMAIL_ADDRESS and EMAIL_PASSWORD.")
    exit()

# ==============================================================================
# --- ⚙️ SETTINGS - CONFIGURE YOUR EVENT HERE ⚙️ ---
# ==============================================================================

# --- Email Sender Details ---
SENDER_NAME = "The JIT Google Student Ambassadors" # The name recipients will see

# --- Email Content Details ---
EVENT_NAME = "Gemini AI Workshop"
EMAIL_SUBJECT = f"🎉 Your Certificate for the {EVENT_NAME} is Here!"
SENDER_ORGANIZATION = "The JIT Google Student Ambassadors Team"
TEAM_MEMBERS_SIGNATURE = "Karan Rathod | Nitisha Naigaokar | Pranav Patil" # Optional: names in the footer

# --- File and Folder Paths ---
# Assumes these files/folders are in the same directory as the script.
STUDENT_LIST_CSV = 'students.csv'
LOGO_IMAGE_PATH = 'logo.jpg'
CERTIFICATES_FOLDER = 'certificates' # Name of the folder containing all PDF certificates

# --- Certificate Filename Format ---
# Use {name} as a placeholder for the student's name.
# The script will replace {name} with the actual student's name from the CSV.
# Example: "John Doe Certificate.pdf"
CERTIFICATE_FILENAME_FORMAT = "{name} Gemini Ai Workshop_ Beginner To Advance.pdf"

# --- SMTP Server Settings (for Gmail) ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# ==============================================================================
# --- 📜 HTML EMAIL TEMPLATE 📜 ---
# ==============================================================================
# Variables like {name}, {event_name}, etc., will be automatically replaced.
html_template = """
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
      <td style="padding: 20px 0;">
        <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; background-color: #ffffff; border: 1px solid #cccccc;">
          <tr>
            <td style="padding: 0; border-top: 5px solid #4285F4;">
              <div style="text-align: center; padding: 20px 0;">
                <img src="cid:logoimage" alt="Organization Logo" style="display: block; max-width: 230px; width: 100%; height: auto; margin: 0 auto;">
              </div>
            </td>
          </tr>
          <tr>
            <td style="padding: 20px 30px; color: #333333; font-size: 16px; line-height: 1.6;">
              <h1 style="color: #4285F4; text-align: center; margin-bottom: 25px;">Congratulations, {name}!</h1>
              <p>On behalf of <b>{sender_organization}</b>, we are thrilled to congratulate you on successfully completing the <b>{event_name}</b>!</p>
              <p>📜 Your official <b>Certificate of Completion</b> is attached to this email. This recognizes your dedication and hard work throughout the session.</p>
              <p>🚀 Keep exploring, keep innovating, and keep building!</p>
            </td>
          </tr>
          <tr>
            <td style="padding: 30px; background-color: #f9f9f9; border-top: 1px solid #eeeeee;">
              <p style="margin: 0; color: #555555; font-size: 14px;">Best regards,</p>
              <p style="margin: 5px 0 10px 0; color: #333333; font-size: 15px;"><b>{sender_organization}</b></p>
              <p style="margin: 0; color: #777777; font-size: 12px;">{team_members_signature}</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""


def send_certificate_emails():
    """
    Sends personalized certificates to a list of students from a CSV file.
    """
    # 1. Login to SMTP Server
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
        print("✅ Successfully logged into the email server.")
    except Exception as e:
        print(f"❌ Error: Could not log into the email server. Please check your credentials in config.py.")
        print(f"   Details: {e}")
        return

    # 2. Prepare the embedded logo image
    try:
        with open(LOGO_IMAGE_PATH, 'rb') as fp:
            img_data = fp.read()
        image_part = MIMEImage(img_data, _subtype='jpeg')
        image_part.add_header('Content-ID', '<logoimage>')
    except FileNotFoundError:
        print(f"❌ Error: Logo image not found at '{LOGO_IMAGE_PATH}'.")
        return

    # 3. Read students CSV and send emails
    sent_count = 0
    error_count = 0
    try:
        with open(STUDENT_LIST_CSV, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                student_name, student_email = row

                # Create the email message container
                msg = MIMEMultipart('related')
                msg['From'] = formataddr((SENDER_NAME, config.EMAIL_ADDRESS))
                msg['To'] = student_email
                msg['Subject'] = EMAIL_SUBJECT

                # Format the HTML body with personalized details
                html_body = html_template.format(
                    name=student_name.title(),
                    event_name=EVENT_NAME,
                    sender_organization=SENDER_ORGANIZATION,
                    team_members_signature=TEAM_MEMBERS_SIGNATURE
                )
                msg.attach(MIMEText(html_body, 'html'))
                msg.attach(image_part) # Attach the logo

                # Find and attach the certificate
                certificate_filename = CERTIFICATE_FILENAME_FORMAT.format(name=student_name.title())
                certificate_path = os.path.join(CERTIFICATES_FOLDER, certificate_filename)

                if os.path.exists(certificate_path):
                    try:
                        with open(certificate_path, "rb") as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(certificate_path)}")
                        msg.attach(part)

                        # Send the email
                        server.send_message(msg)
                        print(f"✔️ Successfully sent certificate to {student_name} at {student_email}")
                        sent_count += 1
                    except Exception as e:
                        print(f"⚠️ Error sending email to {student_name}: {e}")
                        error_count += 1
                else:
                    print(f"❌ Error: Certificate for {student_name} not found at {certificate_path}")
                    error_count += 1

    except FileNotFoundError:
        print(f"❌ Error: Student list not found at '{STUDENT_LIST_CSV}'. Please check the file path.")
        server.quit()
        return

    server.quit()
    print("\n--- Email Sending Complete ---")
    print(f"Total emails sent successfully: {sent_count}")
    print(f"Total errors encountered: {error_count}")

if __name__ == '__main__':
    send_certificate_emails()
