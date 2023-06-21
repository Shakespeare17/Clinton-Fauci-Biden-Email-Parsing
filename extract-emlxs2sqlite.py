import os
import re
import sqlite3
import sys

def create_database():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Create tables if they don't exist
    c.execute('''CREATE TABLE IF NOT EXISTS emails
                 (email text PRIMARY KEY)''')
    c.execute('''CREATE TABLE IF NOT EXISTS phone_numbers
                 (phone_number text PRIMARY KEY)''')
    c.execute('''CREATE TABLE IF NOT EXISTS names
                 (name text PRIMARY KEY)''')
    c.execute('''CREATE TABLE IF NOT EXISTS addresses
                 (address text PRIMARY KEY)''')

    conn.commit()
    conn.close()

def insert_data_into_table(data_set, table_name):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    for data in data_set:
        c.execute(f"INSERT OR IGNORE INTO {table_name} VALUES (?)", (data,))

    conn.commit()
    conn.close()

def extract_data_from_emlxs(directory):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\b(\+\d{1,2}\s?)?(\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}\b'
    name_pattern = r'[A-Z][a-zA-Z\s]+'
    address_pattern = r'\d+\s+[^,]+,[^,]+,[^,]+,\s*\d+'

    email_set = set()
    phone_set = set()
    name_set = set()
    address_set = set()

    for filename in os.listdir(directory):
        if filename.endswith('.emlx'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='latin1') as file:
                content = file.read()

                emails = re.findall(email_pattern, content)
                email_set.update(emails)

                phones = re.findall(phone_pattern, content)
                phone_set.update(phones)

                names = re.findall(name_pattern, content)
                name_set.update(names)

                addresses = re.findall(address_pattern, content)
                address_set.update(addresses)

    return email_set, phone_set, name_set, address_set

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide the directory path as an argument.")
        sys.exit(1)

    directory_path = sys.argv[1]

    if not os.path.isdir(directory_path):
        print("Invalid directory path.")
        sys.exit(1)

    create_database()

    emails, phones, names, addresses = extract_data_from_emlxs(directory_path)

    insert_data_into_table(emails, 'emails')
    insert_data_into_table(phones, 'phone_numbers')
    insert_data_into_table(names, 'names')
    insert_data_into_table(addresses, 'addresses')