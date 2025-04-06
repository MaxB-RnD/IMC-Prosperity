# Import the necessary classes from your datamodel and trading agent code
from datamodel import *
from round_0 import *

# Set up some mock data to create a TradingState
def create_mock_trading_state():
    # Mock the order depths for the products
    order_depths = {
        "RAINFOREST_RESIN": OrderDepth(),
        "KELP": OrderDepth()
    }

    # Add some mock buy and sell orders for RAINFOREST_RESIN and KELP
    order_depths["RAINFOREST_RESIN"].buy_orders = {100: 10, 101: 5, 102: 8}
    order_depths["RAINFOREST_RESIN"].sell_orders = {110: 15, 111: 7, 112: 4}

    order_depths["KELP"].buy_orders = {200: 20, 201: 15, 202: 5}
    order_depths["KELP"].sell_orders = {210: 10, 211: 12, 212: 5}

    # Mock the other necessary data (position, trades, etc.)
    position = {"RAINFOREST_RESIN": 10, "KELP": 5}
    own_trades = {}
    market_trades = {}
    observations = Observation({}, {})

    # Create and return the TradingState object
    return TradingState(
        traderData="test_data",
        timestamp=1234567890,
        listings={},
        order_depths=order_depths,
        own_trades=own_trades,
        market_trades=market_trades,
        position=position,
        observations=observations
    )

# Create a mock trading state
state = create_mock_trading_state()

# Instantiate a Trader and run it with the mock state
trader = Trader()
result, conversions, trader_data = trader.run(state)

# Print the results
print("Result:", result)
print("Conversions:", conversions)
print("Trader Data:", trader_data)