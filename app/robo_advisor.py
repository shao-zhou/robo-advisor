# app/robo_advisor.py

import csv
import requests
import json 
import os
import time
from dotenv import load_dotenv

load_dotenv()

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

#
#INFO INPUTS
#

api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
#print(api_key)

try:
    symbol = input("Please specify a stock symbol (e.g. MSFT) and press enter: ")

    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)  # parse json into a dictionary
    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
# print(type(response))  #this is a Response
# print(response.status_code)  #200
# print(response.text)

except KeyError:
    print("Sorry, couldn't find any trading data for that stock symbol. Please try again.")
    exit()

# used Key Error exception handling outlined here: https://python101.pythonlibrary.org/chapter7_exception_handling.html

tsd = parsed_response["Time Series (Daily)"]
dates = list(tsd.keys())
latest_day = dates[0] #assume first day is top; to do: sort to ensure latest day is first
latest_close = tsd[latest_day]["4. close"]


# get high price from each day
# high_prices = [10, 20, 30, 5] # maximum of all high prices
# recent_high = max(high_prices)

high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[latest_day]["2. high"]
    low_price = tsd[latest_day]["3. low"]
    high_prices.append(float(high_price))
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)

#
# INFO OUTPUTS
#

# csv_file_path = "data/prices.csv"
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"],
            })

print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")

print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")

now = time.strftime("%Y-%m-%d %H:%M:%p")
# used code to format date and time suggested in this stackoverflow thread: https://stackoverflow.com/questions/31955761/converting-python-string-to-datetime-obj-with-am-pm
print("REQUEST AT: " + str(now))
print("-------------------------")

print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")

print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")

print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


