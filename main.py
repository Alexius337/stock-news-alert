from pip._vendor import requests
from twilio.rest import Client
from newsapi import NewsApiClient
import time
import config

STOCK = "LMT"
COMPANY_NAME = "Lockheed Martin Corp"

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
stock_open = float(stock_today["1. open"])
stock_close = float(stock_today["4. close"])

acceptable_daily_change = float(stock_open) / 100
stock_change = stock_close - stock_open
stock_message = ""

if stock_open > stock_close + acceptable_daily_change:
    stock_message += STOCK +": " + "🔻" + " " + str(round(stock_change, 2)) + "%\n" + "\n"
    #print(f"The price of {STOCK} {COMPANY_NAME} has dropped significantly.")
elif stock_open < stock_close + acceptable_daily_change:
    stock_message += STOCK +": " + "🔺" + " " + str(round(stock_change, 2)) + "%\n" + "\n"
    #print(f"The price of {STOCK} {COMPANY_NAME} has risen significantly.")

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

news_api_key = config.news_api_key

newsapi = NewsApiClient(api_key=news_api_key)
all_articles = newsapi.get_everything(q=COMPANY_NAME, from_param=date_today, to=date_today, language='en')

for article in all_articles["articles"][0:3]:
    stock_message =  stock_message + article["title"] + "\n"
    stock_message =  stock_message + article["url"] + "\n" + "\n"

print(stock_message)

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

client = Client(account_sid, auth_token)
message = client.messages.create(
    to=outgoing_number, 
    from_=twilio_number,
    body=stock_message
    )
print(message.status)

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

