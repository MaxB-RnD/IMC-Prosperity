import csv
import matplotlib.pyplot as plt
from datamodel import OrderDepth, TradingState, Observation, ConversionObservation
from round_5_offical import Trader

# Load Historical Market States
def load_order_book_data(file_path):
    with open(file_path, newline='') as f:
        reader = csv.DictReader(f, delimiter=';')
        data_by_timestamp = {}
        for row in reader:
            ts = int(row['timestamp'])
            product = row['product']
            if ts not in data_by_timestamp:
                data_by_timestamp[ts] = {}
            if product not in data_by_timestamp[ts]:
                data_by_timestamp[ts][product] = OrderDepth()
            order_depth = data_by_timestamp[ts][product]

            for i in range(1, 4):
                price = row.get(f'bid_price_{i}')
                vol = row.get(f'bid_volume_{i}')
                if price and vol:
                    order_depth.buy_orders[int(price)] = int(vol)
            for i in range(1, 4):
                price = row.get(f'ask_price_{i}')
                vol = row.get(f'ask_volume_{i}')
                if price and vol:
                    order_depth.sell_orders[int(price)] = int(vol)
        return data_by_timestamp

def load_trade_data(file_path):
    with open(file_path, newline='') as f:
        reader = csv.DictReader(f, delimiter=';')
        trades_by_ts = {}
        for row in reader:
            ts = int(row['timestamp'])
            symbol = row['symbol']
            price = float(row['price'])
            qty = int(row['quantity'])

            if ts not in trades_by_ts:
                trades_by_ts[ts] = []
            trades_by_ts[ts].append((symbol, price, qty))
        return trades_by_ts

# Load sunlight index, sugar price, tariffs, etc.
def load_observation_data(file_path):
    with open(file_path, newline='') as f:
        reader = csv.DictReader(f, delimiter=',')
        obs_by_ts = {}
        for row in reader:
            ts = int(row['timestamp'])

            obs_by_ts[ts] = {
                "MAGNIFICENT_MACARONS": ConversionObservation(
                    bidPrice=float(row["bidPrice"]),
                    askPrice=float(row["askPrice"]),
                    transportFees=float(row["transportFees"]),
                    exportTariff=float(row["exportTariff"]),
                    importTariff=float(row["importTariff"]),
                    sugarPrice=float(row["sugarPrice"]),
                    sunlightIndex=float(row["sunlightIndex"])
                )
            }
        return obs_by_ts

def run_backtest(orderbook_data, trade_data, observation_data):
    trader = Trader()

    position = {p: 0 for p in [
        "RAINFOREST_RESIN", "KELP", "SQUID_INK",
        "PICNIC_BASKET1", "PICNIC_BASKET2",
        "VOLCANIC_ROCK", "MAGNIFICENT_MACARONS",
        "VOLCANIC_ROCK_VOUCHER_9500", "VOLCANIC_ROCK_VOUCHER_9750",
        "VOLCANIC_ROCK_VOUCHER_10000", "VOLCANIC_ROCK_VOUCHER_10250",
        "VOLCANIC_ROCK_VOUCHER_10500"
    ]}

    pnl = {k: 0.0 for k in position}
    pnl_over_time = []
    timestamps = []

    for ts in sorted(orderbook_data.keys()):
        state = TradingState(
            traderData="",
            timestamp=ts,
            listings={},
            order_depths=orderbook_data[ts],
            own_trades={},
            market_trades={},
            position=position,
            observations=Observation({}, observation_data.get(ts, {}))  # second arg = conversionObservations
        )

        orders, conversions, _ = trader.run(state)

        for product, order_list in orders.items():
            for order in order_list:
                volume = order.quantity
                price = order.price
                if price is None or price in [float("inf"), float("-inf")]:
                    continue
                if order.quantity > 0:
                    pnl[product] -= price * volume
                    position[product] += volume
                else:
                    pnl[product] += price * (-volume)
                    position[product] += volume

        total_pnl = sum(pnl.values())
        pnl_over_time.append(total_pnl)
        timestamps.append(ts)

    return pnl, position, timestamps, pnl_over_time, conversions


def run_test():
    # Load data for day 2
    orderbook_data2 = load_order_book_data("Performance Data/Historic Data/prices_round_5_day_2.csv")
    trade_data2 = load_trade_data("Performance Data/Historic Data/trades_round_5_day_2.csv")
    obs_data2 = load_observation_data("Performance Data/Historic Data/observations_round_5_day_2.csv")
    pnl2, final_position2, ts2, pnl_over_time2, conversions2 = run_backtest(orderbook_data2, trade_data2, obs_data2)

    # Load data for day 3
    orderbook_data3 = load_order_book_data("Performance Data/Historic Data/prices_round_5_day_3.csv")
    trade_data3 = load_trade_data("Performance Data/Historic Data/trades_round_5_day_3.csv")
    obs_data3 = load_observation_data("Performance Data/Historic Data/observations_round_5_day_3.csv")
    pnl3, final_position3, ts3, pnl_over_time3, conversions3 = run_backtest(orderbook_data3, trade_data3, obs_data3)

    # Load data for day 4
    orderbook_data4 = load_order_book_data("Performance Data/Historic Data/prices_round_5_day_4.csv")
    trade_data4 = load_trade_data("Performance Data/Historic Data/trades_round_5_day_4.csv")
    obs_data4 = load_observation_data("Performance Data/Historic Data/observations_round_5_day_4.csv")
    pnl4, final_position4, ts4, pnl_over_time4, conversions4 = run_backtest(orderbook_data4, trade_data4, obs_data4)

    # Merging results: Combine PnL, final positions, and time series
    combined_pnl = {**pnl2, **pnl3, **pnl4}
    combined_final_position = {**final_position2, **final_position3, **final_position4}
    combined_ts = ts2 + ts3 + ts4
    combined_pnl_over_time = pnl_over_time2 + pnl_over_time3 + pnl_over_time4
    combined_conversions = conversions2 + conversions3 + conversions4  # Combine conversions from all days

    # Print PnL Summary
    print("PnL Summary:")
    for product, value in combined_pnl.items():
        if product == "MAGNIFICENT_MACARONS":
            print(f"Conversions Made: {combined_conversions}")
        else:
            print(f"{product}: {value:.2f} seashells")

    # Print Final Positions
    print("\nFinal Positions:")
    print(combined_final_position)

    return combined_ts, combined_pnl_over_time
