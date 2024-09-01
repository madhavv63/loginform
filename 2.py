import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import re  # Regular expression library

# Database connection setup
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',       # Change as needed
            database='login',
            user='root',            # Change to your MySQL username
            password='8082326156'   # Change to your MySQL password
        )
        return connection
    except Error as e:
        messagebox.showerror("Database Error", f"Error connecting to the database: {e}")
        return None

# Password strength checker
def check_password_strength(password):
    if len(password) < 8:
        return "Weak: Password should be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return "Weak: Password should contain at least one uppercase letter."
    if not re.search(r"[0-9]", password):
        return "Weak: Password should contain at least one digit."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Weak: Password should contain at least one special character."
    return "Strong"

# Sign Up function
def sign_up():
    username = entry_username.get()
    password = entry_password.get()

    if username == "" or password == "":
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    password_strength = check_password_strength(password)
    if "Weak" in password_strength:
        messagebox.showwarning("Password Strength", password_strength)
        return

    try:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            connection.commit()
            messagebox.showinfo("Success", "User registered successfully!")
            entry_username.delete(0, tk.END)
            entry_password.delete(0, tk.END)
        connection.close()
    except Error as e:
        messagebox.showerror("Database Error", f"Error occurred: {e}")

# Login function
def login():
    username = entry_username.get()
    password = entry_password.get()

    if username == "" or password == "":
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    try:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()
            if result:
                messagebox.showinfo("Success", "Login successful!")
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        connection.close()
    except Error as e:
        messagebox.showerror("Database Error", f"Error occurred: {e}")

# Tkinter setup
root = tk.Tk()
root.title("Sign Up and Login")

# Username label and entry
label_username = tk.Label(root, text="Username")
label_username.grid(row=0, column=0, padx=10, pady=10)
entry_username = tk.Entry(root)
entry_username.grid(row=0, column=1, padx=10, pady=10)

# Password label and entry
label_password = tk.Label(root, text="Password")
label_password.grid(row=1, column=0, padx=10, pady=10)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=10)

# Password strength label
label_password_strength = tk.Label(root, text="")
label_password_strength.grid(row=2, column=1, padx=10, pady=10)

def update_password_strength():
    password = entry_password.get()
    strength = check_password_strength(password)
    label_password_strength.config(text=strength)

entry_password.bind("<KeyRelease>", lambda event: update_password_strength())

# Sign Up button
btn_signup = tk.Button(root, text="Sign Up", command=sign_up)
btn_signup.grid(row=3, column=0, padx=10, pady=10)

# Login button
btn_login = tk.Button(root, text="Login", command=login)
btn_login.grid(row=3, column=1, padx=10, pady=10)

# Start the Tkinter main loop
root.mainloop()
