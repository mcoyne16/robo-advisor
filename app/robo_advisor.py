# this is the "app/robo_advisor.py" file

import csv
import json
import os
import datetime
import seaborn as sns
import matplotlib.pyplot as plt

from dotenv import load_dotenv
import requests
from pandas import read_csv

load_dotenv()

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)
#
#INFO INPUTS
#

tickers = []
additional_stocks = True
while additional_stocks == True:
    ticker = input("Please enter a stock symbol, or type 'DONE' if you have finished:  ")
    if ticker.lower() == "done":
        additional_stocks = False
    else:
        tickers.append(ticker)
done = False
# boolean loop to exit reference: https://stackoverflow.com/questions/3357255/python-exit-out-of-two-loops
for ticker in tickers:
    #isnumeric reference: https://www.programiz.com/python-programming/methods/string/isnumeric
    #also discussed isnumeric strategy with Niko Restifo
    numeric_ticker = False
    for i in range(len(ticker)):
        if ticker[i].isnumeric():
            print(f"'{ticker.upper()}' is not valid. Expecting a properly-formed stock symbol like 'MSFT'. Please try again")
            done = True
            break
    if numeric_ticker == True:
        continue
    if len(ticker) > 5:
        print(f"'{ticker.upper()}' is not valid. Expecting a properly-formed stock symbol like 'MSFT'. Please try again")
        continue
    if done:
        break
    api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
#print(api_key)
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}"
    response = requests.get(request_url)
#print(type(response)) # class 'requests.models.response'
#print(response.status_code)
#print(response.text)
    if "Error Message" in response.text:
        print(f"Error, could not locate url.  Please try again.")
        continue
    if "higher API call frequency" in response.text:
        print("You entered too many stocks.  Please try again.")
        quit()
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

#recommendation
    if float(latest_close) <= float(recent_low)* 1.2:
        recommendation = "BUY"
        reason = "The stock's latest closing is less than 20% above its recent low"
    else:
        recommendation = "SELL"
        reason = "The stock's latest closing is greater than 20% above its recent low"

#OUTPUTS
#

    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", f"prices_{ticker}.csv")
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
    date = datetime.date.today()
    time = datetime.datetime.now()
    print("REQUEST AT:", date, time.strftime("%I:%M:%S %p"))
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

#line graph of csv data for past 100 days

    csv_filename = os.path.join(os.path.dirname(__file__), "..", "data", f"prices_{ticker}.csv")
    line_graph = input("Would you like to view a line graph plotting the prices of the stock over time? [y]/n : ")
    if line_graph == "y":
        prices_df = read_csv(csv_filename)
        #seaborn and matplotlib combo attributed to Prof Rossetti slack comment from December 3, 2020
        sns.lineplot(data=prices_df, x="timestamp", y="close")
        #same attribution^
        plt.title(f"Price of {ticker.upper()} stock over the past 100 days")
        plt.xticks(rotation = 90, fontsize=3)
        plt.show()
    else:
        print("-------------------------")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")