# app/robo_advisor.py

import requests
import json 
import time

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

#
#INFO INPUTS
#

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"
response = requests.get(request_url)
# print(type(response))  #this is a Response
# print(response.status_code)  #200
# print(response.text)

parsed_response = json.loads(response.text)  # parse json into a dictionary

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]
dates = list(tsd.keys())
latest_day = dates[0] #assume first day is top; to do: sort to ensure latest day is first
latest_close = tsd[latest_day]["4. close"]


# get high price from each day
# high_prices = [10, 20, 30, 5] # maximum of all high prices
# recent_high = max(high_prices)

high_prices = []

for date in dates:
    high_price = tsd[latest_day]["2. high"]
    high_prices.append(float(high_price))

recent_high = max(high_prices)

#
# INFO OUTPUTS
#


print("-------------------------")
print("SELECTED SYMBOL: XYZ")

print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")

now = time.strftime("%Y-%m-%d %H:%M:%p")
# used code to format date and time suggested in this stackoverflow thread: https://stackoverflow.com/questions/31955761/converting-python-string-to-datetime-obj-with-am-pm
print("REQUEST AT: " + str(now))
print("-------------------------")

print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print("RECENT LOW: $99,000.00")

print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")

print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")