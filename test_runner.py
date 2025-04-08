import csv
from datamodel import OrderDepth, TradingState, Observation
from round_0 import Trader

# Load historical market states
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

# Run the backtest with error handling
def run_backtest(orderbook_data, trade_data):
    trader = Trader()
    position = {"RAINFOREST_RESIN": 0, "KELP": 0, "SQUID_INK": 0}
    pnl = {"RAINFOREST_RESIN": 0.0, "KELP": 0.0, "SQUID_INK": 0.0}

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

        try:
            orders, conversions, _ = trader.run(state)
        except (OverflowError, ValueError, ZeroDivisionError, TypeError) as e:
            #print(f"[Warning] Skipping timestamp {ts} due to error: {e}")
            continue

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

    return pnl, position

# Load everything and run it
orderbook_data = load_order_book_data("Performance Data/Historic Data/prices_round_1_day_0.csv")
trade_data = load_trade_data("Performance Data/Historic Data/trades_round_1_day_0.csv")
pnl, final_position = run_backtest(orderbook_data, trade_data)

print("PnL Summary:")
for product in pnl:
    print(f"{product}: {pnl[product]:.2f} seashells")

print("\nFinal Positions:")
print(final_position)