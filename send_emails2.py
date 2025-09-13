import os
import smtplib
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
from email.utils import formataddr # <-- ADD THIS IMPORT to fix the sender name

def send_certificate_emails():
    """
    Sends certificates to a list of students from a CSV file using a professional,
    responsive HTML template with an embedded image.
    """
    # --- Configuration ---
    your_email = "karankailashrathod0@gmail.com"
    your_password = "xfbt ihwa mmhm gbcn"  # Use your App Password here
    sender_name = "JIT Google Student Ambassadors" # <-- ADD SENDER NAME HERE

    # --- Email Content ---
    subject = "🎉 Your Certificate from the JIT GSA Team is Here!"

    # --- NEW: Professional HTML Template with Google Color Theme ---
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
                    <img src="cid:logoimage" alt="JIT GSA Logo" style="display: block; max-width: 230px; width: 100%; height: auto; margin: 0 auto;">
                  </div>
                </td>
              </tr>
              <tr>
                <td style="padding: 20px 30px; color: #333333; font-size: 16px; line-height: 1.6;">
                  <h1 style="color: #4285F4; text-align: center; margin-bottom: 25px;">Congratulations, {name}!</h1>
                  <p>On behalf of the <b>JIT Google Student Ambassadors</b>, we are thrilled to congratulate you on successfully completing the <b>Gemini AI Workshop</b>!</p>
                  <p>📜 Your official <b>Certificate of Completion</b> is attached to this email. This recognizes your dedication and hard work throughout the session.</p>
                  <p>💡 Your active participation and curiosity truly stood out. We are confident that you will continue to achieve great things in the world of Artificial Intelligence.</p>
                  <p>🚀 Keep exploring, keep innovating, and keep building!</p>
                </td>
              </tr>
              <tr>
                <td style="padding: 30px; background-color: #f9f9f9; border-top: 1px solid #eeeeee;">
                  <p style="margin: 0; color: #555555; font-size: 14px;">Best regards,</p>
                  <p style="margin: 5px 0 10px 0; color: #333333; font-size: 15px;"><b>The JIT Google Student Ambassadors Team</b></p>
                  <p style="margin: 0; color: #777777; font-size: 12px;">Karan Rathod | Nitisha Naigaokar | Pranav Patil</p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """

    # --- File Paths ---
    logo_image_path = r'C:\Users\karan\OneDrive\Desktop\logo.jpg'
    certificates_folder = r'C:\Users\karan\Downloads\All Certificates for Gemini AI Workshop 2025-20250912T163805Z-1-001\Cleaned Certificates'
    student_list_csv = r'C:\Users\karan\OneDrive\Desktop\students.csv'

    # --- SMTP Server Settings (for Gmail) ---
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # --- Main Logic ---
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(your_email, your_password)
        print("✅ Successfully logged into the email server.")
    except Exception as e:
        print(f"❌ Error: Could not log into the email server. Please check your email and App Password.")
        print(f"   Details: {e}")
        return

    try:
        with open(logo_image_path, 'rb') as fp:
            img_data = fp.read()
    except FileNotFoundError:
        print(f"❌ Error: Logo image not found at '{logo_image_path}'.")
        return

    # Create the image part once
    image = MIMEImage(img_data, _subtype='jpeg')
    image.add_header('Content-ID', '<logoimage>')

    with open(student_list_csv, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            student_name, student_email = row
            
            msg = MIMEMultipart('related')
            # --- FIX: Set the sender name and email address ---
            msg['From'] = formataddr((sender_name, your_email))
            msg['To'] = student_email
            msg['Subject'] = subject
            
            html_body = html_template.format(name=student_name.title()) # .title() to properly capitalize name
            msg.attach(MIMEText(html_body, 'html'))
            
            msg.attach(image)
            
            certificate_filename = f"{student_name.title()} Gemini Ai Workshop_ Beginner To Advance.pdf"
            certificate_path = os.path.join(certificates_folder, certificate_filename)
            
            if os.path.exists(certificate_path):
                try:
                    with open(certificate_path, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(certificate_path)}")
                    msg.attach(part)
                    
                    server.send_message(msg)
                    print(f"✔️ Successfully sent certificate to {student_name} at {student_email}")
                
                except Exception as e:
                    print(f"⚠️ Error sending email to {student_name}: {e}")
            else:
                print(f"❌ Error: Certificate for {student_name} not found at {certificate_path}")

    server.quit()
    print("\nEmail sending process complete.")

if __name__ == '__main__':
    send_certificate_emails()