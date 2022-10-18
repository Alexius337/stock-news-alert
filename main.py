from urllib import response
from pip._vendor import requests
from twilio.rest import Client
import config

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# Twilio authentication and account information
account_sid = config.twilio_account_sid
auth_token  = config.twilio_api_token
twilio_number = config.my_twilio_number
outgoing_number = config.outgoing_number

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

stock_message = ""

client = Client(account_sid, auth_token)
message = client.messages.create(
    to=outgoing_number, 
    from_=twilio_number,
    body=stock_message
    )

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

