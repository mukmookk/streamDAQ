# provide a ticker to the url API
# provide a key
# provide a outpath / serverless request / save database

# import pandas lib as pd
import pandas as pd
from apiCall import earnings
import os

apikey = os.getenv('APIKEY')
pathway = r"./outputfolder/"

# read by default 1st sheet of an excel file
dataframe1 = pd.read_excel('streaming/sample/SteelIndustry.xlsx')
print(dataframe1)
list_of_tickers = dataframe1['Ticker'].to_numpy()

print(earnings(apikey, list_of_tickers, pathway))