import kalshi_python
from KalshiClientsBaseV2 import ExchangeClient
import time
import json
import uuid

ticker = 'HIGHNY-23OCT09-B60.5'
demo_email = "ketanss@bu.edu" # change these to be your personal credentials
demo_password = "Ketankalshi2001#" # (for extra security, we recommend using a config file)
demo_api_base = "https://demo-api.kalshi.co/trade-api/v2"
exchange_client = ExchangeClient(exchange_api_base = demo_api_base, email = demo_email, password = demo_password)
contracts = 1
price=1
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