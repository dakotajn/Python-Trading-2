
# Dak. Sponsored by Concur. Fuck excel, use Concur.

# Pandas for handling Alpha Vantage API return
# Alpha Vantage for free stock pulls (5 per minute)
# MatPlotLib plotting return values from Alpha Vantage

import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
from twilio.rest import Client

# Alpha Vantage API Key:
alpha_key = 'I5R7SASD9D1YXR3X'

# Twilio setup for texting
account_sid = 'ACe83cab8e3e97c2e901d73c70807a2524'
twilio_key = '396f177ea8e8c2d410413b2a84b6ce60'
client = Client(account_sid, twilio_key)
text_body = "default"
text_to = "+12069148960"
text_from = "+12057518820"

period_count = 3 * 60
sma_smoothing = period_count / 6

# Test pull SQ Stock Prices and plot the last hour of prices
ts = TimeSeries(key=alpha_key, output_format='pandas')
data_ts, meta_data_ts = ts.get_intraday(symbol='SQ', interval='1min', outputsize='full')

# Get SMA for SQ from Alpha Vantage
ti = TechIndicators(key=alpha_key, output_format='pandas')
data_ti, meta_data_ti = ti.get_sma(symbol='SQ', interval='1min', time_period=int(round(sma_smoothing)),
                                   series_type='close')

close_prices = data_ts['4. close'][:period_count]
pct_change = close_prices.pct_change()
sq_sma = data_ti['SMA'][-period_count:]

print()
print("Size of each list:")
print()
print("data_ti: " + str(len(data_ti)))
print("data_ts: " + str(len(data_ts)))
print("close_prices: " + str(len(close_prices)))
print("pct_change: " + str(len(pct_change)))
print("sq_sma: " + str(len(data_ti['SMA'][-period_count:])))

table_b = pd.concat([close_prices, sq_sma], axis=1)
table_b.plot()
# plt.show()

text_body = "BUY SQ RIGHT NOW YOU CACK @ $" + str(data_ts['4. close'][0])

# Text ya boi (1550 free texts)
message = client.messages.create(body=text_body, from_=text_from, to=text_to)
print()
print("Message: " + text_body + " | SENT TO: " + text_to)

