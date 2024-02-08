import requests
import datetime as dt
import os
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHAVANTAGE_API_KEY = 'GGBOXIZNYRXWEMKP'
ALPHAVANTAGE_END_POINT = 'https://www.alphavantage.co/query'
NEWS_API_KEY = 'c892c61b7eff4d70b2335d9de845ec1d'
NEWS_API_ENDPOINT = 'https://newsapi.org/v2/everything'
FROM = 'whatsapp:+14155238886'
TWILLO_ACCOUNT_SID = 'AC6225dcec0dc9d7ba1c300b82be9af3a2'
TWILLO_AUTH_TOKEN = os.environ.get('TWILLO_AUTH_TOKEN')
TO = 'whatsapp:+923422469246'

alphavantage_params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': 'TSLA',
    'apikey': 'GGBOXIZNYRXWEMKP'
}

response = requests.get(ALPHAVANTAGE_END_POINT, params=alphavantage_params)
response.raise_for_status()

today = dt.datetime.now()
yesterday = today - dt.timedelta(days=1)
db_yesterday = today - dt.timedelta(days=2)
yesterday_str = yesterday.strftime("%Y-%m-%d")
db_yesterday_str = db_yesterday.strftime("%Y-%m-%d")
data = response.json()
yesterday_close = float(data["Time Series (Daily)"][yesterday_str]["4. close"])
db_yesterday_close = float(data["Time Series (Daily)"][db_yesterday_str]["4. close"])

perc_change = ((yesterday_close - db_yesterday_close) / db_yesterday_close) * 100
if abs(perc_change) <= 2:
    news_params = {
    'q': COMPANY_NAME,
    'from': db_yesterday_str,
    'sortBy': 'publishedAt',
    'language': 'en',
    'apiKey': NEWS_API_KEY
}
    response = requests.get(NEWS_API_ENDPOINT, params=news_params)
    articles = response.json()['articles'][:3]
    if perc_change > 0:
        symbol = '🔺'
    else:
        symbol = '🔻'
    msgs = []
    for article in articles:
        msg = f"""{STOCK}: {symbol}{round(perc_change, 1)}%
Headline: {article['title']}. 
Brief: {article['description']}."""
        msgs.append(msg)

    client = Client(TWILLO_ACCOUNT_SID, TWILLO_AUTH_TOKEN)
    for msg in msgs:
        message = client.messages.create(
            from_=FROM,
            body=msg,
            to=TO
        )
        print(message.status)


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


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

