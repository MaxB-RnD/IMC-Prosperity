import csv
import matplotlib.pyplot as plt
from datamodel import OrderDepth, TradingState, Observation
from round_4_offical import Trader


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
            # Parse bid orders
            for i in range(1, 4):
                price = row.get(f'bid_price_{i}')
                vol = row.get(f'bid_volume_{i}')
                if price and vol:
                    order_depth.buy_orders[int(price)] = int(vol)
            # Parse ask orders
            for i in range(1, 4):
                price = row.get(f'ask_price_{i}')
                vol = row.get(f'ask_volume_{i}')
                if price and vol:
                    order_depth.sell_orders[int(price)] = int(vol)
        return data_by_timestamp


# Load executed trades (historical prices)
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


# Run the backtest and track PnL at each timestamp
def run_backtest(orderbook_data, trade_data):
    trader = Trader()
    
    position = {
    "RAINFOREST_RESIN": 0, "KELP": 0, "SQUID_INK": 0,
    "PICNIC_BASKET1": 0, "PICNIC_BASKET2": 0,
    "VOLCANIC_ROCK": 0,
    "VOLCANIC_ROCK_VOUCHER_9500": 0,
    "VOLCANIC_ROCK_VOUCHER_9750": 0,
    "VOLCANIC_ROCK_VOUCHER_10000": 0,
    "VOLCANIC_ROCK_VOUCHER_10250": 0,
    "VOLCANIC_ROCK_VOUCHER_10500": 0,
    }

    pnl = {
        "RAINFOREST_RESIN": 0.0, "KELP": 0.0, "SQUID_INK": 0.0,
        "PICNIC_BASKET1": 0.0, "PICNIC_BASKET2": 0.0,
        "VOLCANIC_ROCK": 0.0,
        "VOLCANIC_ROCK_VOUCHER_9500": 0.0,
        "VOLCANIC_ROCK_VOUCHER_9750": 0.0,
        "VOLCANIC_ROCK_VOUCHER_10000": 0.0,
        "VOLCANIC_ROCK_VOUCHER_10250": 0.0,
        "VOLCANIC_ROCK_VOUCHER_10500": 0.0,
    }

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
            observations=Observation({}, {})
        )

        # Run the Algorithm
        orders, conversions, _ = trader.run(state)

        # Simulate execution: assume orders are filled at the top of book
        for product, order_list in orders.items():
            for order in order_list:
                volume = order.quantity
                price = order.price
                if price is None or price == float("inf") or price == float("-inf"):
                    print(f"[Debug] Skipping invalid price order at ts {ts}: {price}")
                    continue
                if order.quantity > 0:
                    # Buy
                    pnl[product] -= price * volume
                    position[product] += volume
                else:
                    # Sell
                    pnl[product] += price * (-volume)
                    position[product] += volume

        # Track total PnL across all products
        total_pnl = sum(pnl.values())
        pnl_over_time.append(total_pnl)
        timestamps.append(ts)

    return pnl, position, timestamps, pnl_over_time


# Load and backtest each day's data
def run_test():
    orderbook_data0 = load_order_book_data("Performance Data/Historic Data/prices_round_4_day_1.csv")
    trade_data0 = load_trade_data("Performance Data/Historic Data/trades_round_4_day_1.csv")
    pnl0, final_position0, ts0, pnl_over_time0 = run_backtest(orderbook_data0, trade_data0)

    orderbook_data1 = load_order_book_data("Performance Data/Historic Data/prices_round_4_day_2.csv")
    trade_data1 = load_trade_data("Performance Data/Historic Data/trades_round_4_day_2.csv")
    pnl1, final_position1, ts1, pnl_over_time1 = run_backtest(orderbook_data1, trade_data1)

    orderbook_data2 = load_order_book_data("Performance Data/Historic Data/prices_round_4_day_3.csv")
    trade_data2 = load_trade_data("Performance Data/Historic Data/trades_round_4_day_3.csv")
    pnl2, final_position2, ts2, pnl_over_time2 = run_backtest(orderbook_data2, trade_data2)

    # Add totals for PnL
    pnl_total = {}
    for product in pnl0:
        pnl_total[product] = pnl0[product] + pnl1[product] + pnl2[product]

    # Add totals for Final Positions
    final_position_total = {}
    for product in final_position0:
        final_position_total[product] = final_position0[product] + final_position1[product] + final_position2[product]

    # Print Results
    print("PnL Summary:")
    for product in pnl_total:
        print(f"{product}: {pnl_total[product]:.2f} seashells")

    print("\nFinal Positions:")
    print(final_position_total)

    # Combine PnL over time
    combined_ts = ts0 + ts1 + ts2
    combined_pnl = pnl_over_time0 + pnl_over_time1 + pnl_over_time2

    return combined_ts, combined_pnl
