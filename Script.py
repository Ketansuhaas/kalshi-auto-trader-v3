import pandas as pd
import numpy as np
import kalshi_python
from KalshiClientsBaseV2 import ExchangeClient
from statsmodels.tsa.vector_ar.var_model import VAR
import time
import json
import uuid
from meteostat import Stations
from datetime import datetime
from meteostat import Hourly
import pandas as pd
import numpy as np

def get_data(date):
    start = datetime(2018, 1, 1,00,00)
    end = datetime(date.year, date.month, date.day, 3, 59)  
    data = Hourly('KNYC0', start, end)
    data = data.fetch()
    data.to_csv('openmeteodata.csv')
    df = pd.read_csv("openmeteodata.csv")
    df =df.drop(columns=['time','snow','wpgt','tsun','coco'])
    df['temp'] = df['temp'].apply(lambda x: x*(9/5) +32)
    df[df.columns] = df[df.columns].fillna(df[df.columns].mean())
    df.to_csv('openmeteodata.csv')
    return df


def build_predict(df,complexity):
    model = VAR(df)
    results = model.fit(complexity)
    forecast_period = 24
    forecast = results.forecast(df.values, steps=forecast_period)
    prediction = max(forecast[:,0])
    return  round(prediction)

def get_ticker_id(tickers,prediction):
    tickers_ranges = [float(x.split('-')[-1][1:]) for x in tickers]
    for i in range(1,len(tickers_ranges)-1):
        tickers_ranges[i] = [tickers_ranges[i]-0.5,tickers_ranges[i]+0.5]
    tickers_ranges[0] = [-20,tickers_ranges[0]-1]
    tickers_ranges[-1] = [tickers_ranges[-1]+1,150]
    for i in range(len(tickers_ranges)):
        if prediction>=tickers_ranges[i][0] and prediction<=tickers_ranges[i][1]:
            return i
        
def get_suitable_ticker(prediction,demo_email,demo_password,date):
    # demo_email = "ketanss@bu.edu" 
    # demo_password = "Ketankalshi2001#" 
    prod_api_base = "https://trading-api.kalshi.com/trade-api/v2"
    demo_api_base = "https://demo-api.kalshi.co/trade-api/v2"
    exchange_client = ExchangeClient(exchange_api_base = demo_api_base, email = demo_email, password = demo_password)
    event_ticker = "HIGHNY-23OCT"
    if date.day<10:
        event_ticker+= ('0'+str(date.day))
    else:
        event_ticker+= (str(date.day))
        
    event_params = {'event_ticker': event_ticker}
    event_response = exchange_client.get_event(**event_params)
    tickers = []
    for i in event_response['markets']:
        tickers.append(i['ticker'])
    tickers_modified = [x.split('-')[-1] for x in tickers]
    best_ticker = get_ticker_id(tickers_modified,prediction)
    return tickers[best_ticker], exchange_client

def make_trade(best_ticker,exchange_client,contracts,price):
    ticker = best_ticker
    order_params = {'ticker':ticker,
                    'client_order_id':str(uuid.uuid4()),
                    'type':'limit',
                    'action':'buy',
                    'side':'yes',
                    'count':contracts,
                    'yes_price':price, # yes_price = 100 - no_price
                    'no_price':None, # no_price = 100 - yes_price
                    'expiration_ts':None,
                    'sell_position_floor':None,
                    'buy_max_cost':None}

    exchange_client.create_order(**order_params)

# def main():
#     df = get_data(date)
#     pred = 63 #build_predict(df)
#     ticker,ex = get_suitable_ticker(pred)
#     make_trade(ticker,ex)


# if __name__ == "__main__":
#     main()


