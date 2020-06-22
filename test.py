import yfinance as yf

import ssl
ssl._create_default_https_context = ssl._create_unverified_context
msft = yf.Ticker("MSFT")

# get stock info
print(msft.info)