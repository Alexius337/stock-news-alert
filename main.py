from pip._vendor import requests
from twilio.rest import Client
from newsapi import NewsApiClient
import time
import config

# Choose stock and company name to track
STOCK = "LEGN"
COMPANY_NAME = "Legend Biotech Corporation"

# Twilio authentication and account information
account_sid = config.twilio_account_sid
auth_token  = config.twilio_api_token
twilio_number = config.my_twilio_number
outgoing_number = config.outgoing_number

# Today's date:
date_today = time.strftime("%Y-%m-%d")

# Stock API endpoint and auth
stock_api_endpoint = "https://www.alphavantage.co/query?"
stock_api_key = config.stock_price_api_key

# Stock API params
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "datatype" : "json",
    "apikey": stock_api_key,
}

# Send request to stock API
stock_response = requests.get(stock_api_endpoint, params=stock_params)
stock_response.raise_for_status()

# Process stock API response data
stock_data = stock_response.json()
stock_today = stock_data["Time Series (Daily)"][date_today]
stock_open = float(stock_today["1. open"])
print(stock_open)
stock_close = float(stock_today["4. close"])
print(stock_close)

acceptable_daily_change = stock_open / 100
stock_change = stock_close - stock_open
stock_message = ""

# Custom message for weather stock increased or decreased
if stock_open > stock_close + acceptable_daily_change:
    stock_message += STOCK +": " + "🔻" + " " + str(round(stock_change, 2)) + "%\n" + "\n"

elif stock_open < stock_close + acceptable_daily_change:
    stock_message += STOCK +": " + "🔺" + " " + str(round(stock_change, 2)) + "%\n" + "\n"

# News API auth
news_api_key = config.news_api_key

# Send request to news API
newsapi = NewsApiClient(api_key=news_api_key)
all_articles = newsapi.get_everything(q=COMPANY_NAME, from_param=date_today, to=date_today, language='en')

# Add 3 most recent news articles for our stock to the message
for article in all_articles["articles"][0:3]:
    stock_message =  stock_message + article["title"] + "\n"
    stock_message =  stock_message + article["url"] + "\n" + "\n"

# Verify the message locally that we plan to send
print(stock_message)

# Twilio SMS auth
client = Client(account_sid, auth_token)

# Twilio send SMS with our message
#message = client.messages.create(
    #to=outgoing_number, 
    #from_=twilio_number,
    #body=stock_message
    #)

# Check message status
#print(message.status)
