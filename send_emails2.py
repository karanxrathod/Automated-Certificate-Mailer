import os
import smtplib
import csv
import time
import logging
import argparse
import re
from datetime import datetime
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
    print("💡 Tip: Copy config.example.py to config.py and update with your credentials.")
    exit()

# ==============================================================================
# --- ⚙️ SETTINGS - CONFIGURE YOUR EVENT HERE ⚙️ ---
# ==============================================================================

# --- Email Sender Details ---
SENDER_NAME = "The JIT Google Student Ambassadors"

# --- Email Content Details ---
EVENT_NAME = "Gemini AI Workshop"
EMAIL_SUBJECT = f"🎉 Your Certificate for the {EVENT_NAME} is Here!"
SENDER_ORGANIZATION = "The JIT Google Student Ambassadors Team"
TEAM_MEMBERS_SIGNATURE = "Siddhesh Suryawanshi | Karan Rathod | Nitisha Naigaokar"

# --- File and Folder Paths ---
STUDENT_LIST_CSV = 'students.csv'
LOGO_IMAGE_PATH = 'logo.jpg'
CERTIFICATES_FOLDER = 'certificates'
LOG_FOLDER = 'logs'

# --- Certificate Filename Format ---
CERTIFICATE_FILENAME_FORMAT = "{name} Gemini Ai Workshop_ Beginner To Advance.pdf"

# --- SMTP Server Settings (for Gmail) ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- Retry Settings ---
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# ==============================================================================
# --- 📜 HTML EMAIL TEMPLATE 📜 ---
# ==============================================================================
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

# ==============================================================================
# --- 🔧 UTILITY FUNCTIONS ---
# ==============================================================================

def setup_logging(verbose=False):
    """Setup logging configuration with file and console handlers."""
    if not os.path.exists(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)
    
    log_filename = os.path.join(LOG_FOLDER, f'email_sender_{datetime.now().strftime("%Y%m%d")}.log')
    
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_configuration(logger):
    """Validate all required files and configurations exist."""
    logger.info("🔍 Validating configuration...")
    
    errors = []
    
    # Check config credentials
    if not hasattr(config, 'EMAIL_ADDRESS') or not hasattr(config, 'EMAIL_PASSWORD'):
        errors.append("config.py missing EMAIL_ADDRESS or EMAIL_PASSWORD")
    elif not validate_email(config.EMAIL_ADDRESS):
        errors.append(f"Invalid email format in config.py: {config.EMAIL_ADDRESS}")
    
    # Check files exist
    if not os.path.exists(STUDENT_LIST_CSV):
        errors.append(f"Student list not found: {STUDENT_LIST_CSV}")
    
    if not os.path.exists(LOGO_IMAGE_PATH):
        errors.append(f"Logo image not found: {LOGO_IMAGE_PATH}")
    
    if not os.path.exists(CERTIFICATES_FOLDER):
        errors.append(f"Certificates folder not found: {CERTIFICATES_FOLDER}")
    
    if errors:
        logger.error("❌ Configuration validation failed:")
        for error in errors:
            logger.error(f"   - {error}")
        return False
    
    logger.info("✅ Configuration validation passed!")
    return True

def progress_bar(current, total, bar_length=40, prefix='Progress'):
    """Display a progress bar in the console."""
    percent = float(current) * 100 / total
    arrow = '=' * int(percent/100 * bar_length - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    
    print(f'\r{prefix}: [{arrow}{spaces}] {current}/{total} ({percent:.1f}%)', end='', flush=True)

# ==============================================================================
# --- 📧 EMAIL SENDING FUNCTIONS ---
# ==============================================================================

def send_certificate_emails(dry_run=False, delay=0, retry_attempts=MAX_RETRIES, verbose=False):
    """
    Sends personalized certificates to a list of students from a CSV file.
    
    Args:
        dry_run (bool): If True, validates setup without sending emails
        delay (int): Seconds to wait between emails (rate limiting)
        retry_attempts (int): Number of retry attempts for failed emails
        verbose (bool): Enable verbose logging
    """
    logger = setup_logging(verbose)
    
    # Validate configuration
    if not validate_configuration(logger):
        return
    
    if dry_run:
        logger.info("🧪 DRY-RUN MODE: No emails will be sent.")
    
    # Statistics
    stats = {
        'total': 0,
        'sent': 0,
        'errors': 0,
        'skipped': 0
    }
    failed_emails = []
    
    # 1. Login to SMTP Server (skip in dry-run)
    server = None
    if not dry_run:
        try:
            logger.info("🔐 Logging into email server...")
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
            logger.info("✅ Successfully logged into the email server.")
        except Exception as e:
            logger.error(f"❌ Error: Could not log into the email server.")
            logger.error(f"   Details: {e}")
            logger.error("💡 Tip: Make sure you're using an App Password, not your regular Gmail password.")
            return
    
    # 2. Prepare the embedded logo image
    try:
        with open(LOGO_IMAGE_PATH, 'rb') as fp:
            img_data = fp.read()
        image_part = MIMEImage(img_data, _subtype='jpeg')
        image_part.add_header('Content-ID', '<logoimage>')
        logger.info(f"✅ Logo image loaded: {LOGO_IMAGE_PATH}")
    except FileNotFoundError:
        logger.error(f"❌ Error: Logo image not found at '{LOGO_IMAGE_PATH}'.")
        if server:
            server.quit()
        return
    
    # 3. Read students CSV and process
    try:
        with open(STUDENT_LIST_CSV, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            students = list(reader)
            stats['total'] = len(students)
            
            logger.info(f"📋 Found {stats['total']} students in {STUDENT_LIST_CSV}")
            
            for idx, row in enumerate(students, 1):
                student_name, student_email = row
                
                # Validate email format
                if not validate_email(student_email):
                    logger.warning(f"⚠️ Invalid email format: {student_email} for {student_name}")
                    stats['skipped'] += 1
                    continue
                
                # Progress bar
                progress_bar(idx, stats['total'], prefix='Sending Certificates')
                
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
                msg.attach(image_part)
                
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
                        
                        # Send the email (skip in dry-run)
                        if not dry_run:
                            success = False
                            for attempt in range(retry_attempts):
                                try:
                                    server.send_message(msg)
                                    logger.info(f"✔️ Successfully sent certificate to {student_name} at {student_email}")
                                    stats['sent'] += 1
                                    success = True
                                    break
                                except Exception as e:
                                    if attempt < retry_attempts - 1:
                                        logger.warning(f"⚠️ Retry {attempt + 1}/{retry_attempts} for {student_name}: {e}")
                                        time.sleep(RETRY_DELAY)
                                    else:
                                        logger.error(f"❌ Failed after {retry_attempts} attempts for {student_name}: {e}")
                                        stats['errors'] += 1
                                        failed_emails.append((student_name, student_email, str(e)))
                            
                            # Rate limiting
                            if delay > 0 and idx < stats['total']:
                                time.sleep(delay)
                        else:
                            logger.info(f"✔️ [DRY-RUN] Would send to {student_name} at {student_email}")
                            stats['sent'] += 1
                    
                    except Exception as e:
                        logger.error(f"⚠️ Error processing email for {student_name}: {e}")
                        stats['errors'] += 1
                        failed_emails.append((student_name, student_email, str(e)))
                else:
                    logger.error(f"❌ Error: Certificate for {student_name} not found at {certificate_path}")
                    stats['errors'] += 1
                    failed_emails.append((student_name, student_email, "Certificate file not found"))
    
    except FileNotFoundError:
        logger.error(f"❌ Error: Student list not found at '{STUDENT_LIST_CSV}'. Please check the file path.")
        if server:
            server.quit()
        return
    
    # Cleanup
    if server:
        server.quit()
    
    # Final statistics
    print()  # New line after progress bar
    logger.info("\n" + "="*60)
    logger.info("📊 EMAIL SENDING SUMMARY")
    logger.info("="*60)
    logger.info(f"Total students: {stats['total']}")
    logger.info(f"✅ Successfully sent: {stats['sent']}")
    logger.info(f"❌ Errors encountered: {stats['errors']}")
    logger.info(f"⏭️ Skipped (invalid email): {stats['skipped']}")
    
    if failed_emails:
        logger.info("\n❌ Failed Emails:")
        for name, email, error in failed_emails:
            logger.info(f"   - {name} ({email}): {error}")
    
    logger.info("="*60)
    
    if dry_run:
        logger.info("\n🧪 Dry-run complete! Run without --dry-run to send actual emails.")

# ==============================================================================
# --- 🚀 MAIN ENTRY POINT ---
# ==============================================================================

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Automated Certificate Mailer - Send personalized certificates via email',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python send_emails2.py                    # Send emails to all students
  python send_emails2.py --dry-run          # Test without sending
  python send_emails2.py --delay 2          # Add 2-second delay between emails
  python send_emails2.py --retry 5          # Retry failed emails 5 times
  python send_emails2.py --verbose          # Enable verbose logging
        '''
    )
    
    parser.add_argument('--dry-run', action='store_true',
                        help='Test mode - validate setup without sending emails')
    parser.add_argument('--delay', type=int, default=0, metavar='SECONDS',
                        help='Delay between emails in seconds (rate limiting)')
    parser.add_argument('--retry', type=int, default=MAX_RETRIES, metavar='N',
                        help=f'Number of retry attempts for failed emails (default: {MAX_RETRIES})')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Enable verbose logging')
    
    args = parser.parse_args()
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║         📧 Automated Certificate Mailer v2.0 📧             ║
    ║                                                              ║
    ║  Original Author: Karan Rathod                              ║
    ║  Enhanced by: Siddhesh Suryawanshi                          ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    send_certificate_emails(
        dry_run=args.dry_run,
        delay=args.delay,
        retry_attempts=args.retry,
        verbose=args.verbose
    )
