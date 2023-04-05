from alpha_vantage.timeseries import TimeSeries
import time
import requests
import json
from pandas import json_normalize
import pandas as pd

def earnings(key, list_of_tickers, output_path):
    """
    key = API key from Alpha Vantage
    list_of_tickers = list of tickers to be used
    output_path = path to output folder
    
    return dataframe of earnings data
    """
    # counter
    i = 0
    # create empty dataframe
    df2 = pd.DataFrame()

    for ticker in list_of_tickers:
        print(ticker)
        i = i + 1
        url = 'https://www.alphavantage.co/query?function=EARNINGS&symbol={}&interval=1min&apikey={}'.format(ticker, key)
        
        # # requestion our URL string is passed here and converting the response to a dictionary
        response = requests.get(url)
        response_dict = response.json()
        start_time = time.time()

        try:
            # select the data from the dictionary
            selected_json = response_dict['quarterlyEarnings']
            print(selected_json)
        except:
            print("No data for this ticker")
            continue
        
        time_waited = 0
        while time.time() - start_time < 12:
            time_waited += 1
            time.sleep(1)
        print("Waiting for {} seconds".format(time_waited))
        
        try:
            # convert the dictionary to a dataframe
            df = pd.DataFrame.from_dict(json_normalize(selected_json), orient='columns')
            df.to_csv(output_path + 'file_quarterly_earnings_{}.csv'.format(ticker))
        except:
            print("Can not convert json to csv")
            continue
    return "Successfully queried {} tickers".format(i)

