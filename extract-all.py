import sys
import re
import sqlite3

def extract_info(input_file):
    db_file = f"{input_file}_info.db"

    # Check if the file exists
    try:
        with open(input_file) as file:
            file_content = file.read()
    except FileNotFoundError:
        print("File does not exist.")
        return

    # Connect to the SQLite database
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS extracted_info (
                        id INTEGER PRIMARY KEY,
                        recipient TEXT,
                        sender TEXT,
                        subject TEXT,
                        message TEXT
                    )''')

    # Extract the fields using regex
    matches = re.findall(r'To:\s*(.*?)\s*From:\s*(.*?)\s*Sender:\s*(.*?)\s*Subject:\s*(.*?)\s*\$(.*?)\s*(?=\nTo:|\Z)',
                         file_content, re.DOTALL)

    # Insert the extracted information into the database
    for match in matches:
        recipient, sender, email_sender, subject, message = match
        cursor.execute("INSERT INTO extracted_info (recipient, sender, subject, message) VALUES (?, ?, ?, ?)",
                       (recipient.strip(), sender.strip(), email_sender.strip(), subject.strip(), message.strip()))

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

    print(f"Information extracted and saved to {db_file}.")


# Main script execution starts here

if len(sys.argv) > 1:
    input_file = sys.argv[1]
    extract_info(input_file)
else:
    print("Please provide a file path.")