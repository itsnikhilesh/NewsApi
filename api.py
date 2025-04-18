import csv
import bcrypt
import validators
import re
import requests
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

# File to store user data
USER_DATA_FILE = 'user_auth.csv'
API_KEY = 'c4ed6f8faee9494aa6be3eb6f36ed2ce'

def validate_email(email):
    return validators.email(email)

def validate_password(password):
    return len(password) >= 8 and re.search(r"\W", password)

def register_user():
    email = simpledialog.askstring("Register", "Enter email:")
    if not validate_email(email):
        messagebox.showerror("Error", "Invalid email format.")
        return

    password = simpledialog.askstring("Register", "Enter password:", show='*')
    if not validate_password(password):
        messagebox.showerror("Error", "Password must be at least 8 characters with a special character.")
        return

    security_q = simpledialog.askstring("Security Question", "Set your security question:")

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    file_exists = os.path.isfile(USER_DATA_FILE)

    with open(USER_DATA_FILE, 'a', newline='') as file:
        fieldnames = ['email', 'password', 'security_question']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({'email': email, 'password': hashed_password.decode('utf-8'), 'security_question': security_q})

    messagebox.showinfo("Success", "Registration successful!")

def login_user():
    email = simpledialog.askstring("Login", "Enter email:")
    password = simpledialog.askstring("Login", "Enter password:", show='*')
    if not validate_email(email):
        messagebox.showerror("Error", "Invalid email format.")
        return False

    try:
        with open(USER_DATA_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['email'] == email:
                    if bcrypt.checkpw(password.encode(), row['password'].encode()):
                        messagebox.showinfo("Success", "Login successful!")
                        keyword = simpledialog.askstring("News", "Enter a keyword:")
                        fetch_news(keyword)
                        return True
                    else:
                        messagebox.showerror("Error", "Incorrect password.")
                        return False
            messagebox.showerror("Error", "Email not found.")
    except FileNotFoundError:
        messagebox.showerror("Error", "User data file not found.")
    return False

def reset_password():
    email = simpledialog.askstring("Reset Password", "Enter your registered email:")
    try:
        with open(USER_DATA_FILE, 'r') as file:
            users = list(csv.DictReader(file))
        for row in users:
            if row['email'] == email:
                answer = simpledialog.askstring("Security Check", f"{row['security_question']}:")
                if answer.lower() == row['security_question'].lower():
                    new_password = simpledialog.askstring("New Password", "Enter new password:", show='*')
                    if validate_password(new_password):
                        hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
                        update_password_in_csv(email, hashed)
                        messagebox.showinfo("Success", "Password reset successful!")
                    else:
                        messagebox.showerror("Error", "Password doesn't meet requirements.")
                    return
        messagebox.showerror("Error", "Email or answer is incorrect.")
    except FileNotFoundError:
        messagebox.showerror("Error", "User data file not found.")

def update_password_in_csv(email, new_hashed_password):
    users = []
    with open(USER_DATA_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['email'] == email:
                row['password'] = new_hashed_password.decode('utf-8')
            users.append(row)

    with open(USER_DATA_FILE, 'w', newline='') as file:
        fieldnames = ['email', 'password', 'security_question']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(users)

def fetch_news(keyword):
    url = f'https://newsapi.org/v2/everything?q={keyword}&apiKey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        news = response.json()
        articles = news.get('articles', [])
        if articles:
            news_text = "\n\n".join([f"{i+1}. {a['title']} ({a['source']['name']})" for i, a in enumerate(articles[:5])])
            messagebox.showinfo("Top News", news_text)
        else:
            messagebox.showinfo("No News", "No articles found.")
    else:
        messagebox.showerror("Error", "Failed to fetch news. Check API key or network.")

# GUI Setup
root = tk.Tk()
root.title("News App with Login System")
root.geometry("350x300")
root.resizable(False, False)

tk.Label(root, text="Welcome to News App", font=("Arial", 16)).pack(pady=20)

tk.Button(root, text="Register", command=register_user, width=25, pady=5).pack(pady=5)
tk.Button(root, text="Login", command=login_user, width=25, pady=5).pack(pady=5)
tk.Button(root, text="Forgot Password", command=reset_password, width=25, pady=5).pack(pady=5)
tk.Button(root, text="Exit", command=root.destroy, width=25, pady=5).pack(pady=20)

root.mainloop()