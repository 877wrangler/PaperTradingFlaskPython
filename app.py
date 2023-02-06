import requests
import finnhub
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from flask_session import Session
import os
import sqlite3
from dotenv import load_dotenv

# Get API
dotenv_path = "C:/Users/Randy/PycharmProjects/FlashPythonPaperTrading/api.env"
load_dotenv(dotenv_path)
api_key = os.getenv("API_KEY")
finnhub_client = finnhub.Client(api_key=api_key)

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Open database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

@app.route("/")
# @login_required
def index():
    # user_id = session["user_id"]
    # print(user_id)
    # account_info = db.execute("SELECT * FROM account WHERE user_id LIKE ?", (user_id))
    # print(account_info)
    # data = []
    # for row in account_info:
    #     data.append(row)
    #     print(row)
    # print(data)
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    register_username = request.form.get("register_username")
    register_password = request.form.get("register_password")

    if request.method == "POST":
        # Check if the username exists
        username_exists = cursor.execute("SELECT username FROM users WHERE username = ?", (register_username))

        # If the username doesn't exist, hash the password and insert the data
        if not username_exists:
            password_hash = generate_password_hash(register_password)
            print(password_hash)
            cursor.execute("INSERT INTO users (username, hash, cash) VALUES (?, ?, ?)", register_username, password_hash, 10000)
            conn.commit()
            return redirect("/login")

    return render_template("register.html")


@app.route("/quote", methods=["GET", "POST"])
# @login_required
def quote():
    """Get stock quote."""
    ticker = request.form.get("quote")
    latest_price = None
    if request.method == "POST":
        quote = finnhub_client.quote(ticker)
        latest_price = quote['c']
        print(latest_price)

    return render_template("quote.html", latest_price=latest_price, ticker=ticker)




if __name__ == '__main__':
    app.run()