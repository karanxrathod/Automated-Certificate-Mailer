# Automated Certificate Mailer 📧✨

A Python-based automation tool to send personalized certificates to participants of a workshop or event. This project reads a list of students from a CSV, attaches a corresponding certificate PDF, and sends it using a professional HTML email template.

## Features 🚀

- **Bulk Emailing**: Sends emails to a list of recipients from a `students.csv` file.
- **Dynamic Personalization**: Automatically inserts the recipient's name into the email body.
- **HTML Email Templates**: Uses a clean, responsive HTML template for a professional look.
- **PDF Attachments**: Finds and attaches a unique certificate for each student.
- **Logo Embedding**: Embeds a logo directly into the email body.
- **CSV Management**: Includes a helper script to update and de-duplicate the student list from multiple sources.

## How to Use 📋

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/Automated-Certificate-Mailer.git](https://github.com/YOUR_USERNAME/Automated-Certificate-Mailer.git)
    cd Automated-Certificate-Mailer
    ```

2.  **Create your configuration file:**
    Create a file named `config.py` and add your email credentials:
    ```python
    # config.py
    EMAIL_ADDRESS = "your_email@gmail.com"
    EMAIL_PASSWORD = "your_google_app_password"
    SENDER_NAME = "Your Organization Name"
    ```
    **Note:** You must use a Google App Password, not your regular password.

3.  **Organize your files:**
    - Place your organization's logo (e.g., `logo.jpg`) in the project directory.
    - Place your `students.csv` file in the project directory. It must have `Name,Email` columns.
    - Create a folder (e.g., `certificates/`) and place all certificate PDF files inside.

4.  **Update the paths in `send_emails2.py`** to point to your logo, CSV file, and certificates folder.

5.  **Run the script:**
    ```bash
    python send_emails2.py
    ```

## Scripts Overview 🐍

- **`send_emails2.py`**: The main script that handles the email sending process.
- **`update_students_csv.py`**: A utility script to merge new participant lists into the main `students.csv`, ensuring there are no duplicates.
