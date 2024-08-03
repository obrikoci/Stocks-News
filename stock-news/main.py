import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "api key from stock"
NEWS_API_KEY = "api key from news"

TWILIO_SID = "twilio sid"
TWILIO_AUTH_TOKEN = "auth token"

stocks_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "datatype": "json",
    "apikey": STOCK_API_KEY,
}

news_params = {
    "q": COMPANY_NAME,
    "qInTite": COMPANY_NAME,
    "apiKey": NEWS_API_KEY,
    "language": "en"
}

stocks = requests.get(url=STOCK_ENDPOINT, params=stocks_params)
stocks.raise_for_status()
stock_data = stocks.json()
yesterday_closing_stocks = float(stock_data["Time Series (Daily)"]["2024-04-22"]["4. close"])
prev_day_closing_stocks = float(stock_data["Time Series (Daily)"]["2024-04-19"]["4. close"])


diff = round(yesterday_closing_stocks - prev_day_closing_stocks, 3)
change = None
if diff > 5:
    change = "🔺"
else:
    change = "🔻"

percentage = round(diff/yesterday_closing_stocks * 100, 3)
if abs(percentage) > 1:
    news = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news.json()["articles"]

    three_articles = articles[:3]

    formatted_articles = [f"{STOCK}: {change}{percentage}%\nHeadline: {article['title']}. \nBrief Description: {article['description']}" for article in three_articles]
    print(formatted_articles)
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
                from_="twilio number",
                body=article,
                to="your number"
            )
