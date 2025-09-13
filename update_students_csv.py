import csv
import os

# --- Configuration ---
# Instructions:
# 1. Place the CSV file with the new student registrations in the same folder as this script.
#    Rename it to 'new_registrations.csv' or change the filename below.
# 2. The main student list is named 'students.csv'. This script will create it if it
#    doesn't exist, or update it if it does.

NEW_STUDENTS_FILENAME = 'new_registrations.csv'
EXISTING_STUDENTS_FILENAME = 'students.csv'

# --- Column Configuration for the new registrations file ---
# IMPORTANT: Set the column numbers (indexes) for the name and email.
# The first column is 0, second is 1, and so on.
# From your original script, Name was the 3rd column (index 2) and Email was the 4th (index 3).
NAME_COLUMN_INDEX = 2
EMAIL_COLUMN_INDEX = 3


def update_student_list():
    """
    Reads student info from a new CSV and merges it with the existing students.csv file,
    removing duplicates.
    """
    unique_students = set()
    header = ['Name', 'Email']

    # 1. Read the existing students.csv if it exists
    if os.path.exists(EXISTING_STUDENTS_FILENAME):
        try:
            with open(EXISTING_STUDENTS_FILENAME, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)  # Read the existing header
                for row in reader:
                    if len(row) >= 2:
                        name, email = row[0], row[1]
                        # Add to set with a consistent case for email to handle duplicates
                        unique_students.add((name.strip(), email.strip().lower()))
            print(f"Loaded {len(unique_students)} students from '{EXISTING_STUDENTS_FILENAME}'.")
        except Exception as e:
            print(f"Error reading '{EXISTING_STUDENTS_FILENAME}': {e}")
            return
    else:
        print(f"'{EXISTING_STUDENTS_FILENAME}' not found. A new file will be created.")

    # 2. Read the new student info CSV
    try:
        with open(NEW_STUDENTS_FILENAME, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            newly_added = 0
            for row in reader:
                # Check if the row is long enough to contain the required columns
                if len(row) > max(NAME_COLUMN_INDEX, EMAIL_COLUMN_INDEX):
                    name = row[NAME_COLUMN_INDEX].strip()
                    email = row[EMAIL_COLUMN_INDEX].strip()
                    if name and email:  # Ensure they are not empty strings
                        student_tuple = (name, email.lower())
                        if student_tuple not in unique_students:
                            unique_students.add(student_tuple)
                            newly_added += 1
            print(f"Found {newly_added} new students in '{NEW_STUDENTS_FILENAME}'.")
    except FileNotFoundError:
        print(f"Error: Input file '{NEW_STUDENTS_FILENAME}' not found. Please check the filename and location.")
        return
    except Exception as e:
        print(f"Error reading '{NEW_STUDENTS_FILENAME}': {e}")
        return

    # 3. Write the unique, combined list back to students.csv
    try:
        # Sort the list alphabetically by name for consistency
        sorted_students = sorted(list(unique_students))
        
        with open(EXISTING_STUDENTS_FILENAME, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(sorted_students)
        
        print(f"✅ Successfully updated '{EXISTING_STUDENTS_FILENAME}'. Total unique students: {len(sorted_students)}.")
    except Exception as e:
        print(f"Error writing to '{EXISTING_STUDENTS_FILENAME}': {e}")


if __name__ == '__main__':
    update_student_list()
