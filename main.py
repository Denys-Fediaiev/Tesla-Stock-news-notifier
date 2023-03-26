import os
from datetime import *
from twilio.rest import Client
from twilio import *
from datetime import time

import requests
account_sid = "AC97193163ba42abed9b9d8c19555c6513"
auth_token = '875eaa4dda9a7bd86ffc8e4f7f06fac2'
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
api_key = "WCEPO812YCJSBN1I"

stock_params = {
    "function": "TIME_SERIES_INTRADAY",
    "symbol": STOCK,
    "interval": 5,
    "apikey": api_key,

}
## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={STOCK}&apikey={api_key}'
r = requests.get(url)
stock_data = r.json()["Time Series (Daily)"]
now_date = date.today()
yesterday_date = now_date - timedelta(days=1)
day_before_yesterday = now_date - timedelta(days=2)

if day_before_yesterday.isoweekday() >= 6 or yesterday_date.isoweekday() >= 6:
    print("It's weekend")
else:
    yesterday_close_price = float(stock_data[str(yesterday_date)]["4. close"])
    day_before_yesterday = float(stock_data[str(day_before_yesterday)]["4. close"])
    s = yesterday_close_price - day_before_yesterday

    percent = (s * 100) / yesterday_close_price
    percent = round(percent, 2)

    if percent > 5 or percent < -5:
        response = requests.get(f"https://newsapi.org/v2/everything?q=tesla&from={yesterday_date}&sortBy=publishedAt&"
                                "apiKey=ba734fb2d537440d9e3dcb4b0d0b3f8a")
        response.raise_for_status()
        data = response.json()
        news = [n for n in data["articles"] if data["articles"].index(n) < 3]
        print(f"Tesla close-price in past 2 days = {percent}%\n Check the news:")
        for new in news:
            print(new)
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
            body=f"\nTesla close-price in past 2 days = {percent}%\n\n Check the news:\n"
                 f"Title:\n{news[0]['title']}\n\nNews:\n{news[0]['description']}\n\n"
                 f"Title:\n{news[1]['title']}\n\nNews:\n{news[1]['description']} \n\n"
                 f"Title:\n{news[2]['title']}\n\nNews:\n{news[2]['description']}",
            from_='+14406893664',
            to='+353877174610'
        )

    else:
        print(f"Tesla close-price in past 2 days is {percent}%")

    # if (stock_data[str(day_before_yesterday)]["4. close"] )

## STEP 2: Use https://newsapi.org   Your API key is: ba734fb2d537440d9e3dcb4b0d0b3f8a
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
