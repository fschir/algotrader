import numpy as np
import pandas as pd
from poloniex import poloniex
import po_api
import trader


class Env:
    def __init__(self):
        self.conn = poloniex.Poloniex(po_api.api_key, po_api.secret)
        self.active_trader = trader.Trader()
        self.actions = [
            'BUY_USDC_BTC',
            'BUY_BTC_ETH',
            'BUY_BTC_XMR',
            'BUY_BTC_XRP',
            'BUY_BTC_DOGE',
            'SELL_USDC_BTC',
            'SELL_BTC_ETH',
            'SELL_BTC_XMR',
            'SELL_BTC_XRP',
            'SELL_BTC_DOGE',
        ]
        self.state = []

    def _update_orders(self):
        self.activeOrders = conn.returnOrderBook('all')

    def execute(self, action):
        pass

    def reset(self):
        self.state = []


conn = poloniex.Poloniex(po_api.api_key, po_api.secret)
print(conn.returnOrderBook('all'))
print(conn.returnBalances())

