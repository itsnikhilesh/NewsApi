News App with Login System
📌 Project Overview
This is a Python-based desktop application that allows users to register, log in, reset their password, and fetch the latest news headlines using NewsAPI. The application features a simple and user-friendly GUI built with Tkinter and includes a secure authentication mechanism using hashed passwords.

💡 Key Features
User Registration with email, secure password, and a customizable security question.

User Login system that validates credentials.

Password Reset using the answer to the user's security question.

News Fetching functionality that retrieves the top 5 headlines based on a keyword entered by the user.

Secure Storage of user credentials using password hashing.

Responsive GUI for ease of interaction.

🧰 Tools & Technologies Used
Python – Core programming language

Tkinter – For the graphical user interface

CSV File Handling – To store user credentials

bcrypt – For secure password hashing

validators – For email validation

requests – To connect to the NewsAPI

NewsAPI – For fetching live news articles

📂 File Structure
user_auth.csv – Automatically generated file to store registered users securely.

news_app_gui.py – The main application file (contains all logic and UI).

README.md – Project documentation.

🧠 How It Works
Registration: User provides an email, password, and security question. Input is validated and securely stored.

Login: User logs in using their credentials. Upon success, they can search for news articles by keyword.

Password Reset: If the user forgets their password, they can reset it by answering their previously set security question.

News Search: On successful login, the user is prompted to enter a keyword, and the app fetches the top 5 news headlines from NewsAPI.

🔐 Security Considerations
Passwords are never stored in plain text – they are hashed using bcrypt.

Only valid email formats and secure passwords are accepted during registration.

The system uses a simple file-based approach (CSV) for credential storage, suitable for small-scale applications.

🎯 Use Case
This project is ideal for demonstrating:

Secure authentication logic in a GUI-based app

Integration of real-time data using an API

Basic desktop software development with Python

📜 License
This project is open for personal and educational use. Attribution is appreciated if reused or modified.
