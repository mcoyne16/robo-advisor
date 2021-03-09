# this is the "app/robo_advisor.py" file

import csv
import json
import os
import datetime

from dotenv import load_dotenv
import requests

load_dotenv()

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)
#
#INFO INPUTS
#

tickers = []
tickers.append(input("please enter a stock ticker:"))

#ticker = input("Please enter a stock ticker:")

for ticker in tickers
    numeric_ticker = False
    for i in range(len(ticker)):
        if ticker[i].isnumeric():
            print(f"{ticker.upper()} is not valid. Expecting a properly-formed stock symbol like 'MSFT'. Please try again")
            break
    if numeric_ticker == True:
        continue
    if len(ticker) > 5:
        print(f"{ticker.upper()} is not valid. Expecting a properly-formed stock symbol like 'MSFT'. Please try again")
        continue

api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
print(api_key)
symbol = "IBM" 

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

response = requests.get(request_url)
#print(type(response)) # class 'requests.models.response'
#print(response.status_code)
#print(response.text)
if "Error Message" in response.text:
    print(f"Error, could not locate url.  Please try again.")

parsed_response = json.loads(response.text)
last_refreshed = parsed_response['Meta Data']['3. Last Refreshed']
tsd = parsed_response['Time Series (Daily)']
dates = list(tsd.keys()) #TODO sort
latest_day = dates[0]
latest_close = tsd[latest_day]['4. close']

high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))

recent_high = max(high_prices) 
recent_low = min(low_prices)

if float(latest_close) <= float(recent_low):
    recommendation = "BUY"
    reason = "The stock's latest closing is less than its recent low"
else:
    recommendation = "SELL"
    reason = "The stock's latest closing is greater than its recent low"

#breakpoint()
#quit()
#OUTPUTS
#

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
    #csv_file_path = "data/prices.csv" # a relative filepath

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
print("SELECTED SYMBOL:", ticker.upper())
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print("LATEST DAY: ",last_refreshed)
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}" )
print(f"RECENT LOW: {to_usd(float(recent_low))}" )
print("-------------------------")
print(f"RECOMMENDATION: {recommendation}")
print(f"RECOMMENDATION REASON: {reason}")
print("-------------------------")
print(f"WRITING DATA TO CSV {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

# csv-mgmt/write_teams.py