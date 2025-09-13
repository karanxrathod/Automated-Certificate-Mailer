import csv

def update_student_list():
    """
    Reads student info from a new CSV and merges it with the existing students.csv file,
    removing duplicates.
    """
    new_students_file = r'C:\Users\karan\Downloads\GSA Session 1 Certificate and Review Responses (1).csv'
    existing_students_file = r'C:\Users\karan\OneDrive\Desktop\students.csv'

    # Use a set to store unique (Name, Email) tuples, with email being case-insensitive
    unique_students = set()

    # 1. Read the existing students.csv
    try:
        with open(existing_students_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader) # Keep the header
            for row in reader:
                if len(row) == 2:
                    name, email = row
                    unique_students.add((name.strip(), email.strip().lower()))
    except FileNotFoundError:
        print(f"'{existing_students_file}' not found. Starting with an empty list.")
        header = ['Name', 'Email'] # Create a header if the file doesn't exist
    except Exception as e:
        print(f"Error reading '{existing_students_file}': {e}")
        return

    # 2. Read the new student info CSV
    try:
        with open(new_students_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            for row in reader:
                if len(row) > 3:
                    # Column indices from observation: Name is 3rd, Email is 4th
                    name = row[2].strip()
                    email = row[3].strip()
                    if name and email: # Ensure they are not empty strings
                        unique_students.add((name, email.lower()))
    except FileNotFoundError:
        print(f"Error: '{new_students_file}' not found.")
        return
    except Exception as e:
        print(f"Error reading '{new_students_file}': {e}")
        return

    # 3. Write the unique, combined list back to students.csv
    try:
        with open(existing_students_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            # Sort the result for consistency
            sorted_students = sorted(list(unique_students))
            # Create a new list for writing to avoid duplicate emails with different casing
            final_students = []
            seen_emails = set()
            for name, email in sorted_students:
                if email not in seen_emails:
                    final_students.append([name, email])
                    seen_emails.add(email)
            writer.writerows(final_students)
        print(f"Successfully updated '{existing_students_file}' with {len(final_students)} unique students.")
    except Exception as e:
        print(f"Error writing to '{existing_students_file}': {e}")


if __name__ == '__main__':
    update_student_list()
