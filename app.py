import requests
import finnhub
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from flask_session import Session
import os
import sqlite3
from dotenv import load_dotenv
from helpers import lookup

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
    register_username = request.form.get("register_username")
    register_password = request.form.get("register_password")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":
        # Check if the username exists
        username_exists = cursor.execute("SELECT username FROM users WHERE username = ?", (register_username,)).fetchone()
        print(username_exists)

        # If the username doesn't exist, hash the password and insert the data
        if not username_exists:
            password_hash = generate_password_hash(register_password)
            print(password_hash)
            cursor.execute("INSERT INTO users (username, hash, cash) VALUES (?, ?, ?)", (register_username, password_hash, 10000))
            conn.commit()
            conn.close()
            return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html")

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        rows = cursor.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()

        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            # authentication failed

            return render_template("error.html")

        # Remember which user has logged in
        session["user_id"] = rows[0][0]


        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/buy", methods=["GET", "POST"])
# @login_required
def buy():
    """Buy shares of stock"""
    ticker = request.form.get("ticker")
    amount = request.form.get("amount")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT cash FROM users WHERE id = ?", (session["user_id"],))
    balance = cursor.fetchone()
    cash = balance[0]

    if request.method == "POST":
        # If quote is not empty

        if request.form.get("ticker") and lookup(ticker):
            print(lookup(ticker))
            latest_price = lookup(ticker)['price']
            cost = latest_price * int(amount)
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if cost <= cash:
                cursor.execute("INSERT INTO account (ticker, shares, cost, time, user_id) VALUES (?, ?, ?, ?, ?)",
                               (ticker.upper(), amount, cost, time, session["user_id"]))
                cursor.execute("UPDATE users SET cash = cash - ? WHERE id = ?", (cost, session["user_id"]))
                cash -= cost
                conn.commit()
            conn.close()
            return render_template("buy.html", cash=cash)
        else:
            return render_template("error.html")


    return render_template("buy.html", cash=cash)


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