import requests 
import pandas

#enter your IEX Cloud API Sandbox token here
IEX_CLOUD_API_TOKEN = 

page = pandas.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
stocks_table = page[0]
info = stocks_table.info()

print()

stocks_columns = ["Ticker", "Price", "Market Capitalization", "Shares to Buy"]
stocks_dataframe = pandas.DataFrame(columns = stocks_columns)

#generating 500 individual API calls
for symbol in stocks_table["Symbol"]:
  new_symbol = symbol

  if(symbol == "BRK-B"):
    new_symbol = "BRK.B"

  api_url = f"https://sandbox.iexapis.com/stable/stock/{new_symbol}/quote?token={IEX_CLOUD_API_TOKEN}"
  data = requests.get(api_url).json()
  stocks_dataframe = stocks_dataframe.append(pandas.Series([new_symbol, data["latestPrice"], data["marketCap"], "N/A"], index = stocks_columns), ignore_index = True)
  
# spliting the S&P500 list into 5 individual lists
def split_list(list, number_per_group):
  for index in range(0, len(list), number_per_group):
    yield list[index : index + number_per_group]

stock_symbols_groups = list(split_list(stocks_table["Symbol"], 100))
stock_symbols_strings = []

# joining the split lists together into a string
for index in range(0, len(stock_symbols_groups)):
  stock_symbols_strings.append(",".join(stock_symbols_groups[index]))

batch_stocks_dataframe = pandas.DataFrame(columns = stocks_columns)

# generating 5 batch API calls
for symbol_string in stock_symbols_strings:
  new_symbol_string = symbol_string
  if(symbol == "BRK-B"):
    new_symbol_string = "BRK.B"

  batch_api_call_url = f"https://sandbox.iexapis.com/stable/stock/market/batch/?types=quote&symbols={new_symbol_string}&token={IEX_CLOUD_API_TOKEN}"
  data = requests.get(batch_api_call_url).json()
  for symbol in symbol_string.split(","):
    new_symbol = symbol
    if(symbol == "BRK-B"):
      new_symbol = "BRK.B"

    batch_stocks_dataframe = batch_stocks_dataframe.append(pandas.Series([new_symbol, data[new_symbol]["quote"]["latestPrice"], data[new_symbol]["quote"]["marketCap"], "N/A"], index = stocks_columns), ignore_index = True)

print(batch_stocks_dataframe)
