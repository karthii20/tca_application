import pandas as pd
from datetime import timedelta
from helper.utilities import read_all_files_to_df
pd.options.mode.chained_assignment = None
 
class TCAAnalysis:

    def __init__(self,market_data_path):
        self.df_analytics = pd.DataFrame()
        self.market_data_path = market_data_path
 
    def run(self, trades_df, arrival_latency, benchmark_classes, metric_classes):
        enriched_data = self.enrich_data_with_market_trades(trades_df)
        enriched_data['arrival_time'] = pd.to_datetime(enriched_data['signal_time']) + timedelta(milliseconds=arrival_latency)
        rics = enriched_data['RIC'].unique()
        for ric in rics:
            signals = enriched_data.loc[(enriched_data['RIC'] == ric)]['signal_time'].unique()
            for signal_time in signals:
                trades_ric = enriched_data.loc[((enriched_data['signal_time'] == signal_time) & (enriched_data['RIC'] == ric))]
                trades_before_arrival = trades_ric.loc[trades_ric['arrival_time'] > trades_ric['trade_time']]
                #  # ✅ Debugging Before Filtering
                # print(f"\n🔍 Checking Filtering for RIC: {ric}, Signal Time: {signal_time}")
                # print("Before Filtering:", trades_ric.shape)  # Total trades before filtering

                # Apply filtering
                trades_before_arrival = trades_ric.loc[trades_ric['arrival_time'] > trades_ric['trade_time']]

                # ✅ Debugging After Filtering
                # print("After Filtering:", trades_before_arrival.shape)
                trades_ric = self.calculate_becnmarks(trades_ric, trades_before_arrival,benchmark_classes)
                trades_ric = self.calculate_metrics(trades_ric, metric_classes)
                self.df_analytics = pd.concat([self.df_analytics, trades_ric])
        return self.df_analytics
    def enrich_data_with_market_trades(self,trades_df):
        # print("\n📊 Market Data Sample:\n", trades_df.head())
        if 'trade_time' not in trades_df.columns:
            trades_df['trade_time'] = pd.to_datetime(trades_df['TradDtTm'])
        trades_df['trade_time'] = pd.to_datetime(
            trades_df['trade_time'])
        if 'signal_time' not in trades_df.columns:
            trades_df['signal_time'] = pd.to_datetime(trades_df['BizDt'])
        trades_df['signal_time'] = pd.to_datetime(
            trades_df['signal_time'])     
        if 'arrival_time' not in trades_df.columns:
            trades_df['arrival_time'] = pd.to_datetime(trades_df['OrdrDtTm'])
        if 'order_id' not in trades_df.columns:
            trades_df['order_id'] = trades_df['OrdrRef']
        # if '#RIC' not in trades_df.columns:
        #     trades_df['#RIC'] = trades_df['ISIN']
        if 'venue' not in trades_df.columns:
            trades_df['venue'] = trades_df['Xchg']
        if 'position' not in trades_df.columns:
            trades_df['position'] = trades_df['BuySellInd'].map({'B': 1, 'S': -1})
        if 'broker_id' not in trades_df.columns:
            trades_df['broker_id'] = trades_df['Brkr']
        if 'trader_id' not in trades_df.columns:
            trades_df['trader_id'] = trades_df['UnqTradIdr']
        if 'trade_price' not in trades_df.columns:
            trades_df['trade_price'] = trades_df['Pric']
        if 'trade_volume' not in trades_df.columns:
            trades_df['trade_volume'] = trades_df['TradQty']
        if 'arrival_price' not in trades_df.columns:
            trades_df['arrival_price'] = trades_df['StrkPric']
        if 'Exch Time' not in trades_df.columns:
            trades_df['Exch Time'] = trades_df['TradDtTm']
        if 'RIC' not in trades_df.columns:
            trades_df['RIC'] = trades_df['TckrSymb']
        if 'execution_price' not in trades_df.columns:
            trades_df['execution_price'] = trades_df['Pric']
        if 'currency' not in trades_df.columns:
            trades_df['currency'] = "INR"
        order_df = read_all_files_to_df(self.market_data_path)
        # print("\n📊 Market Data Sample:\n", trades_df.head())
        enriched_data = pd.concat([trades_df, order_df])
        enriched_data.sort_values(by=[ 'RIC', 'trade_time'], inplace=True)
        return enriched_data 
    # def enrich_data_with_market_trades(self, trades_df):
    #     trades_df['trade_time'] = pd.to_datetime(trades_df['trade_time'])
    #     trades_df['signal_time'] = pd.to_datetime(trades_df['signal_time'])

    #     # ✅ Load Market Data
    #     order_df = read_all_files_to_df(self.market_data_path)

        # # 🚨 Debugging: Check if market data exists
        # print("\n📊 Market Data Sample:\n", order_df.head())

        # if order_df.empty:
        #     print("⚠️ Market data is empty! No benchmarks will be calculated.")
        #     return trades_df  # Return trade data alone

        # # ✅ Convert timestamps in Market Data
        # order_df['trade_time'] = pd.to_datetime(order_df['trade_time'], errors='coerce')

        # # ✅ Print Unique RICs in Market Data vs Trade Data
        # print("\n🔍 Unique RICs in Market Data:", order_df['RIC'].unique())
        # print("🔍 Unique RICs in Trade Data:", trades_df['RIC'].unique())

        # # ✅ Print Trade Time Range vs Market Data Range
        # print("\n📅 Trade Data Time Range:", trades_df['trade_time'].min(), "to", trades_df['trade_time'].max())
        # print("📅 Market Data Time Range:", order_df['trade_time'].min(), "to", order_df['trade_time'].max())

        # # ✅ Merge Trade Data with Market Data
        # enriched_data = pd.concat([trades_df, order_df], ignore_index=True)
        # enriched_data.sort_values(by=['RIC', 'trade_time'], inplace=True)

        # print("\n✅ Enriched Data Sample After Merge:\n", enriched_data.head())

        # return enriched_data
 

    def calculate_metrics(self, trades_ric, metric_classes):
        for metric_class in metric_classes:
            metric = metric_class()
            metric_values = metric.calculate(trades_ric)
            trades_ric = self.add_metrics_to_df(trades_ric, metric.name, metric_values)
        return trades_ric

    def calculate_becnmarks(self, trades_ric, trades_before_arrival, benchmark_classes):
        benchmarks = {}
        for benchmark_class in benchmark_classes:
            benchmark = benchmark_class()
            benchmarks[benchmark.name] = benchmark.calculate(trades_before_arrival)
        trades_ric = self.add_benchmarks_to_df(trades_ric, benchmarks)
        return trades_ric

    def add_benchmarks_to_df(self, trades_ric, benchmarks):
        for benchmark, value in benchmarks.items():
            trades_ric.loc[trades_ric['order_id'].notnull(), benchmark] = value
        return trades_ric

    def add_metrics_to_df(self, trades_ric, metric, metric_values):
        if hasattr(metric_values, '__len__'):
            trades_ric[metric] = metric_values
        else:
            trades_ric.loc[trades_ric['order_id'].notnull(), metric] = metric_values
        return trades_ric
