import time
import argparse
import csv
import json
import os
import logging

from poloniex import poloniex
from datetime import date, datetime
from matplotlib import pyplot as plt

import po_api
import hyperparams as hy
from preprocessor import Preprocessor
import pandas as pd
import numpy as np


class Trader:

    def __init__(self, *argv):

        # Optparse
        parser = argparse.ArgumentParser(description='Automated Bitcoin Trading Bot')
        parser.add_argument(
            '-p', '--period',
            type=int,
            default=900,
            dest='period',
            help="candlestick period in seconds; valid values are 300, 900, 1800, 7200, 14400, and 86400",
        )
        parser.add_argument(
            '-c', '--currency',
            type=str,
            default='USDC_BTC',
            dest='currency',
            help='Use a specific currency',
        )
        parser.add_argument(
            '--show-chart', default=False,
            dest='show_chart',
            help='Show chart for debug',
        )
        parser.add_argument(
            '-s', '--start-date', default=str(datetime.timestamp(datetime.fromisoformat('2019-01-05'))),
            type=str,
            dest='start_date',
            help='First Date to print ChartData must be ISO YYYY-MM-DD',
        )
        parser.add_argument(
            '-e', '--end-date', default=str(datetime.timestamp(datetime.now())),
            type=str,
            dest='end_date',
            help='First Date to print ChartData must be ISO YYYY-MM-DD',
        )
        parser.add_argument(
            '-v', '--verbose', default=False,
            type=bool,
            dest='verbose',
            help='Verbose output',
        )
        parser.add_argument(
            '-g', '--get-all-exchanges', default=True,
            type=bool,
            dest='get_all_exchanges',
            help='Using get-all-exchanges will get the entire transaction chart in the specified timeframe.'
                 ' Saved under data/exchange/data.csv',
        )
        parser.add_argument(
            '--dry-run', default=False,
            type=bool,
            dest='dry_run',
            help='Dry run to check how well the model works',
        )
        parser.add_argument(
            '--logging', default=True,
            type=bool,
            dest='logging',
            help='Set logging',
        )

        opts = parser.parse_args(args=argv)

        # Params
        self.currency = opts.currency
        self.period = opts.period
        self.start_date = opts.start_date
        self.end_date = opts.end_date
        self.verbose = opts.verbose
        self.get_all_exchanges = opts.get_all_exchanges
        self.dry_run = opts.dry_run
        self.logging = opts.logging
        self.conn = poloniex.Poloniex(po_api.api_key, po_api.secret)

        # Attributes
        self.current_balance = self.get_balance()
        self.prices = []
        self.historical_data_head = {'date', 'high', 'low', 'open', 'close', 'volume', 'quoteVolume', 'weightedAverage'}
        self.historical_data = []
        self.valid_periods = frozenset([300, 900, 1800, 7200, 14400, 86400])

        # Set up logging
        if self.logging is True:
            logging.basicConfig(filename='logs/logging.log', level=logging.DEBUG)

        # Sanity checks for opts

        if opts.period not in self.valid_periods:
            parser.error('Period must be 300, 900, 1800, 7200, 14400, or 86400')

    def get_historical_data(self):
        if not self.get_all_exchanges:
            self.historical_data = self.conn.returnChartData(
                self.currency,
                self.period,
                self.start_date,
                self.end_date
            )
            print(self.historical_data)
        else:
            for exchange in hy.currency_list:
                self.historical_data.append(self.conn.returnChartData(
                    exchange,
                    self.period,
                    self.start_date,
                    self.end_date
                ))

                data_path = 'data/'+str(exchange)

                if not os.path.exists(data_path):
                    os.makedirs(data_path)

                with open(data_path + '/data.csv', 'w', newline='') as file:
                    writer = csv.DictWriter(file, self.historical_data_head,)
                    writer.writeheader()
                    for exchange_data in self.historical_data:
                        writer.writerows(exchange_data)

            logging.debug('Historical Data written to CSV')

    def get_balance(self):
        return self.conn.returnBalances()

    def buy_order(self, currency_pair, rate, amount):
        """
        :param currency_pair: The major and minor currency defining the market where this buy order should be placed.
        :param rate: The rate to purchase one major unit for this trade.
        :param amount: The total amount of minor units offered in this buy order.
        :return: None
        """
        self.conn.buy(currency_pair, rate, amount)

    def sell_order(self, currency_pair, rate, amount):
        """
        :param currency_pair: The major and minor currency defining the market where this buy order should be placed.
        :param rate: The rate to purchase one major unit for this trade.
        :param amount: The total amount of minor units offered in this buy order.
        :return: None
        """
        self.conn.sell(currency_pair, rate, amount)


if __name__ == '__main__':
    t = Trader('-p 300', '-v True',)
    t.get_historical_data()
    p = Preprocessor('data/USDC_BTC/data.csv')
    p.show_plot()
