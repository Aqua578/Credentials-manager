import re
import csv
import hashlib
from colorama import Fore
import os
import sys

FILE_NAME = "credentials_manager.csv"
FILE_PATH = os.path.join(os.path.dirname(__file__), FILE_NAME)

def remove_blank_lines(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        filtered_lines = [line for line in reader if line and line[0].strip()]

    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(filtered_lines)

def validate_credentials(email, hashed_password):
    with open(FILE_PATH, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["email"] == email and row["password"] == hashed_password:
                return True
    return False

def validate_password_for_login(email):
    while True:
        password = input("Password: ")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if validate_credentials(email, hashed_password):
            return hashed_password
        else:
            print(Fore.RED + "Invalid password. Please try again." + Fore.RESET)

def login():
    while True:
        email = email_validator()

        if email_exists(email):
            hashed_password = validate_password_for_login(email)
            print(Fore.GREEN + "Login successful!" + Fore.RESET)
            return
        else:
            print(Fore.RED + "Email does not exist. Please try again." + Fore.RESET)


def signup():
    while True:
        email = email_validator()
        if not email_exists(email):
            password = password_validator()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            with open(FILE_PATH, "a") as file:
                writer = csv.DictWriter(file, fieldnames=["email", "password"])
                writer.writerow({"email": email, "password": hashed_password})

            print(Fore.GREEN + "Sign-up successful!" + Fore.RESET)
            return
        else:
            print("This email is already taken. Please try another one.")

def email_validator():
    while True:
        email = input("Email: ").strip()
        if re.match(r"^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$", email):
            return email
        else:
            print(Fore.RED + "Invalid e-mail. Please enter a valid e-mail address." + Fore.RESET)

def password_validator():
    while True:
        password = input("Password: ")
        if len(password) < 8:
            print(Fore.RED + "Password should be at least 8 characters long" + Fore.RESET)
        else:
            password_checker1 = re.search(r"(?=.*[a-z])", password)
            password_checker2 = re.search(r"(?=.*[A-Z])", password)
            password_checker3 = re.search(r"(?=.*\d)", password)
            password_checker4 = re.search(r"(?=.*[\W])", password)
            if password_checker1 is None:
                print(Fore.RED + "Password should contain at least 1 lowercase character" + Fore.RESET)
            elif password_checker2 is None:
                print(Fore.RED + "Password should contain at least 1 uppercase character" + Fore.RESET)
            elif password_checker3 is None:
                print(Fore.RED + "Password should contain at least 1 number" + Fore.RESET)
            elif password_checker4 is None:
                print(Fore.RED + "Password should contain at least 1 special character" + Fore.RESET)
            else:
                return password

def email_exists(email):
    with open(FILE_PATH, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["email"] == email:
                return True
    return False

def main():
    try:
        if not os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["email", "password"])

        remove_blank_lines(FILE_PATH)

        print("Welcome to Aquachat!")
        print("1. Log-in")
        print("2. Sign-up")

        prompt = int(input("Please select from the following choices (1/2): "))

        if prompt == 1:
            login()
        elif prompt == 2:
            signup()
        else:
            print("Invalid choice. Please select 1 or 2.")

    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}" + Fore.RESET)

if __name__ == "__main__":
    main()
