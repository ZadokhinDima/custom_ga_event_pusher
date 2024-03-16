import requests
import json
import datetime

def get_price():
    url = 'https://api.monobank.ua/bank/currency'
    currencyCode = 840

    response = requests.get(url)
    response_data = json.loads(response.content)
    price = None

    for data in response_data:
        if data['currencyCodeA'] == currencyCode:
            price = data['rateBuy']
            break

    return price

def send_event_price(price):
    url = 'https://www.google-analytics.com/mp/collect?api_secret=VALpHjvySyKlf-IFAZeFdg&measurement_id=G-4W139PRJ6Y'

    params = {
        "client_id": "currency_tracker",
        "events": [
            {
                "name": "USD_buy_price",
                "params": {
                    "value": str(price)
                }
            }
        ]
    }

    return requests.post(url, json=params)

price = get_price()
response = send_event_price(price)

current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"Price: {price}, GA response Code: {response.status_code}, Timestamp: {current_time}")
