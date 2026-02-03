# config.example.py
# ⚠️ Configuration Template
# 
# Instructions:
# 1. Copy this file to config.py
# 2. Replace the placeholder values with your actual credentials
# 3. Never commit config.py to Git (it's in .gitignore)

# ============================================================================
# EMAIL CONFIGURATION
# ============================================================================

# Your Gmail address
EMAIL_ADDRESS = "your_email@gmail.com"

# Google App Password (NOT your regular Gmail password)
# How to get an App Password:
# 1. Go to https://myaccount.google.com/apppasswords
# 2. Generate a new App Password for "Mail"
# 3. Copy the 16-character password here (format: xxxx xxxx xxxx xxxx)
EMAIL_PASSWORD = "your app password here"

# ============================================================================
# IMPORTANT SECURITY NOTES
# ============================================================================
# - NEVER share this file or commit it to version control
# - Use App Passwords, not your regular Gmail password
# - Enable 2-Factor Authentication on your Google Account
# - Revoke App Passwords when no longer needed
