import os
import requests
import urllib.parse
import finnhub
from dotenv import load_dotenv
from flask import redirect, render_template, request, session


# Get API
dotenv_path = "C:/Users/Randy/PycharmProjects/FlashPythonPaperTrading/api.env"
load_dotenv(dotenv_path)
api_key = os.getenv("API_KEY")
finnhub_client = finnhub.Client(api_key=api_key)

def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        quote = finnhub_client.quote(symbol)
    except requests.RequestException:
        return None

    return {
        "price": float(quote["c"]),
        "symbol": symbol
    }