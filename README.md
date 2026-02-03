# 📧 Automated Certificate Mailer

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Contributions](https://img.shields.io/badge/Contributions-Welcome-orange.svg)

**A professional, production-ready Python tool for sending personalized certificates via email**

Automate your certificate distribution process with style! 🎓✨

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 🎯 Features

- ✅ **Bulk Email Distribution** - Send certificates to hundreds of recipients automatically
- 📊 **Progress Tracking** - Real-time progress bar with detailed statistics
- 🎨 **Professional HTML Templates** - Beautiful, responsive email designs
- 📎 **PDF Attachments** - Automatically attach personalized certificates
- 🖼️ **Embedded Logos** - Brand your emails with organization logos
- 🔄 **Smart Retry Logic** - Automatic retry on failures with exponential backoff
- 🧪 **Dry-Run Mode** - Test your setup without sending real emails
- 📝 **Comprehensive Logging** - Detailed logs for debugging and auditing
- ✔️ **Input Validation** - Prevents common configuration errors
- 🐳 **Docker Support** - Containerized deployment ready
- 🔐 **Secure Credentials** - Environment-based configuration management

---

## 📋 Table of Contents

- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Detailed Setup](#-detailed-setup)
- [Usage Guide](#-usage-guide)
- [Configuration](#-configuration)
- [Features Documentation](#-features-documentation)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Credits](#-credits)
- [License](#-license)

---

## 🔧 Prerequisites

- **Python 3.7+** installed on your system
- **Gmail account** with 2-Factor Authentication enabled
- **Google App Password** (not your regular password)
- Basic knowledge of Python and command line

---

## ⚡ Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/karan/Automated-Certificate-Mailer.git
cd Automated-Certificate-Mailer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up configuration
cp config.example.py config.py
# Edit config.py with your credentials

# 4. Prepare your files
# - Add logo.jpg
# - Add students.csv
# - Add certificates in certificates/ folder

# 5. Test with dry-run
python send_emails2.py --dry-run

# 6. Send emails
python send_emails2.py
```

---

## 📚 Detailed Setup

### Step 1: Get Google App Password

1. Go to your [Google Account Settings](https://myaccount.google.com/)
2. Enable **2-Factor Authentication** (Security → 2-Step Verification)
3. Navigate to [App Passwords](https://myaccount.google.com/apppasswords)
4. Select **Mail** and generate a password
5. Copy the 16-character password (format: `xxxx xxxx xxxx xxxx`)

### Step 2: Configure Credentials

Create `config.py` from the example:

```python
# config.py
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password_here"  # 16-character App Password
```

⚠️ **IMPORTANT**: Never commit `config.py` to Git! It's already in `.gitignore`.

### Step 3: Organize Your Files

```
Automated-Certificate-Mailer/
├── send_emails2.py              # Main email sender
├── update_students_csv.py       # Student list updater
├── config.py                    # Your credentials (keep secret!)
├── students.csv                 # Recipients list
├── logo.jpg                     # Your organization logo
├── certificates/                # Certificate PDFs folder
│   ├── John Doe Certificate.pdf
│   └── Jane Smith Certificate.pdf
└── logs/                        # Auto-generated logs
```

### Step 4: Prepare Student List

Create `students.csv` with this format:

```csv
Name,Email
John Doe,john@example.com
Jane Smith,jane@example.com
```

### Step 5: Add Certificates

- Certificate filenames must match: `{Student Name} {Event Name}.pdf`
- Example: `John Doe Gemini Ai Workshop_ Beginner To Advance.pdf`
- Place all PDFs in the `certificates/` folder

---

## 🎓 Usage Guide

### Basic Usage

```bash
# Send certificates to all students
python send_emails2.py
```

### Advanced Usage

```bash
# Dry-run mode (test without sending)
python send_emails2.py --dry-run

# Send with retry logic
python send_emails2.py --retry 3

# Verbose logging
python send_emails2.py --verbose

# Rate limiting (delay between emails)
python send_emails2.py --delay 2
```

### Update Student List

Merge new registrations into your existing list:

```bash
# Prepare new_registrations.csv with new students
python update_students_csv.py
```

This will:
- ✅ Merge new students with existing list
- ✅ Remove duplicates automatically
- ✅ Sort alphabetically by name

---

## ⚙️ Configuration

### Customizing Your Event

Edit these variables in `send_emails2.py`:

```python
# Email Sender Details
SENDER_NAME = "Your Organization Name"

# Event Details
EVENT_NAME = "Your Event Name"
EMAIL_SUBJECT = f"🎉 Your Certificate for {EVENT_NAME} is Here!"
SENDER_ORGANIZATION = "Your Organization"
TEAM_MEMBERS_SIGNATURE = "Team Member 1 | Team Member 2 | Team Member 3"

# File Paths
STUDENT_LIST_CSV = 'students.csv'
LOGO_IMAGE_PATH = 'logo.jpg'
CERTIFICATES_FOLDER = 'certificates'

# Certificate Filename Format
CERTIFICATE_FILENAME_FORMAT = "{name} {event}.pdf"
```

### Customizing Email Template

The HTML template is in `send_emails2.py` (lines 48-86). Customize:
- Colors and branding
- Email content and messaging
- Footer and signature
- Logo styling

---

## 🚀 Features Documentation

### 1. Progress Bar

Real-time visual feedback with statistics:
```
Sending Certificates: 45/100 [=============>      ] 45% | ETA: 2m 15s
✔️ Success: 43 | ⚠️ Errors: 2
```

### 2. Retry Logic

Automatic retry on failures:
- Exponential backoff strategy
- Configurable retry attempts
- Detailed error logging

### 3. Dry-Run Mode

Test your configuration safely:
```bash
python send_emails2.py --dry-run
```
- Validates all files exist
- Checks email format
- Verifies certificate paths
- **Does NOT send emails**

### 4. Comprehensive Logging

Logs saved to `logs/email_sender_YYYYMMDD.log`:
```
2024-02-03 10:15:32 - INFO - Email sent successfully to john@example.com
2024-02-03 10:15:35 - ERROR - Certificate not found for Jane Smith
2024-02-03 10:15:40 - INFO - Retry attempt 1/3 for jane@example.com
```

### 5. Input Validation

Prevents common errors:
- Email format validation
- File existence checks
- CSV structure validation
- Configuration completeness check

### 6. Rate Limiting

Respect Gmail's limits:
- Configurable delay between emails
- Prevents rate limiting issues
- Safe for large recipient lists

---

## 🐳 Docker Support

Run in a containerized environment:

```bash
# Build Docker image
docker build -t certificate-mailer .

# Run with mounted volumes
docker run -v $(pwd)/certificates:/app/certificates \
           -v $(pwd)/config.py:/app/config.py \
           certificate-mailer
```

---

## 🔍 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `❌ Could not log into email server` | Verify App Password, not regular password |
| `❌ Certificate not found` | Check filename format matches exactly |
| `❌ Logo image not found` | Ensure `logo.jpg` exists in root directory |
| Emails going to spam | Use verified domain or warm up account |
| `❌ config.py not found` | Create from `config.example.py` |
| Rate limit errors | Add `--delay 2` to slow down sending |

### Gmail Limits

- **Free Gmail**: ~500 emails/day
- **Google Workspace**: ~2,000 emails/day
- Use `--delay` flag for large batches

### Debug Mode

Enable verbose logging:
```bash
python send_emails2.py --verbose --dry-run
```

### Check Logs

```bash
# View latest log
tail -f logs/email_sender_$(date +%Y%m%d).log

# Search for errors
grep "ERROR" logs/*.log
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit pull requests

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/Automated-Certificate-Mailer.git
cd Automated-Certificate-Mailer

# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes and test thoroughly

# Commit with descriptive messages
git commit -m "feat: add progress bar with ETA calculation"

# Push to your fork
git push origin feature/your-feature-name

# Create a Pull Request on GitHub
```

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to functions
- Include comments for complex logic
- Write descriptive commit messages

---

## 👥 Credits

### Original Author & Maintainer
**Karan Rathod** - *Project Creator & Lead Developer*
- GitHub: [@karan](https://github.com/karan)
- Original implementation and core architecture

### Contributors
**Siddhesh Suryawanshi** - *Major Enhancements & Documentation*
- GitHub: [@SiddheshSuryawanshi17](https://github.com/SiddheshSuryawanshi17)
- Added: Progress bar, retry logic, dry-run mode, comprehensive documentation, Docker support, logging system, input validation, examples & templates

**Special Thanks**
- JIT Google Student Ambassadors Team
- Nitisha Naigaokar
- Pranav Patil
- All community contributors

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🌟 Show Your Support

If this project helped you, please give it a ⭐️!

---

## 📞 Contact & Support

- 🐛 **Bug Reports**: [Open an Issue](https://github.com/karan/Automated-Certificate-Mailer/issues)
- 💬 **Questions**: [Start a Discussion](https://github.com/karan/Automated-Certificate-Mailer/discussions)
- 📧 **Email**: For sensitive issues only

---

<div align="center">

**Made with ❤️ by the Open Source Community**

[⬆ Back to Top](#-automated-certificate-mailer)

</div>
