import requests
import datetime as dt
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHAVANTAGE_API_KEY = 'GGBOXIZNYRXWEMKP'
ALPHAVANTAGE_END_POINT = 'https://www.alphavantage.co/query'
NEWS_API_KEY = 'c892c61b7eff4d70b2335d9de845ec1d'
NEWS_API_ENDPOINT = 'https://newsapi.org/v2/everything'

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


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

perc_change = ((yesterday_close - db_yesterday_close) / db_yesterday_close) * 100
if abs(perc_change) >= 5:
    print('get news')
else:
    print('dont get news')

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
    
news_params = {
    'q': 'tesla',
    'from': db_yesterday_str,
    'sortBy': 'publishedAt',
    'apiKey': NEWS_API_KEY
}
response = requests.get(NEWS_API_ENDPOINT, params=news_params)
print(response.json())

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

