from pip._vendor import requests
from twilio.rest import Client
import time
from datetime import date, timedelta
import config

STOCK = "MPCFF"
COMPANY_NAME = "Roblox Corp"

# Twilio authentication and account information
account_sid = config.twilio_account_sid
auth_token  = config.twilio_api_token
twilio_number = config.my_twilio_number
outgoing_number = config.outgoing_number

# Today's and yesterday's dates:
date_today = time.strftime("%Y-%m-%d")

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_api_endpoint = "https://www.alphavantage.co/query?"
stock_api_key = config.stock_price_api_key

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "datatype" : "json",
    "apikey": stock_api_key,
}

stock_response = requests.get(stock_api_endpoint, params=stock_params)
stock_response.raise_for_status()

stock_data = stock_response.json()
stock_today = stock_data["Time Series (Daily)"][date_today]
stock_open = stock_today["1. open"]
stock_close = stock_today["4. close"]

acceptable_daily_change = float(stock_open) / 10
stock_change = float(stock_open) - float(stock_close)

if stock_change > acceptable_daily_change:
    print("The stock has dropped significantly.")
elif stock_change < (-acceptable_daily_change):
    print("The price has risen significantly.")
else:
    print("The price has not moved significantly.")


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 



## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

stock_message = ""

#client = Client(account_sid, auth_token)
#message = client.messages.create(
    #to=outgoing_number, 
    #from_=twilio_number,
    #body=stock_message
    #)

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

