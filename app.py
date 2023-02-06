import requests
import finnhub
from flask import Flask, render_template, session, request, jsonify
from flask_session import Session
import os
from dotenv import load_dotenv

dotenv_path = "C:/Users/Randy/PycharmProjects/FlashPythonPaperTrading/api.env"
load_dotenv(dotenv_path)
api_key = os.getenv("API_KEY")
print(api_key)
# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

finnhub_client = finnhub.Client(api_key=api_key)

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