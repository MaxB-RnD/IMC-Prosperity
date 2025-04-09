### A TUTORIAL ROUND TEST FILE

# Import Required Libraries
import json
import numpy as np
import math
from typing import Any

# Import the Platform's Provided Classes and Types
from datamodel import * 

# Used for Gaussian Distribution Modeling if Needed
from statistics import NormalDist 



# CLASS FOR TRACKING MARKET STATUS AND HISTORICAL DATA
class Status:
    # Static Variables Shared Across all Instances
    _state = None  # Holds the current trading state
    _num_data = 0  # Counter to track the number of updates

    # Position imits for Different Products
    _position_limit = {
        "RAINFOREST_RESIN": 50,
        "KELP": 50,     
        "SQUID_INK": 50,        
    }

    # Real-time Position for each Product Initialised to 0
    _realtime_position = {key: 0 for key in _position_limit.keys()}

    # Historical Order Depths for Each Product Initialised with Empty Lists
    _hist_order_depths = {
        product: {
            'bidprc1': [], 'bidamt1': [],  # Bid price and amount at level 1
            'bidprc2': [], 'bidamt2': [],  # Bid price and amount at level 2
            'bidprc3': [], 'bidamt3': [],  # Bid price and amount at level 3
            'askprc1': [], 'askamt1': [],  # Ask price and amount at level 1
            'askprc2': [], 'askamt2': [],  # Ask price and amount at level 2
            'askprc3': [], 'askamt3': [],  # Ask price and amount at level 3
        } for product in _position_limit.keys()
    }


    def __init__(self, product: str) -> None:
        """
        Initialises the Status object with a given product.
        
        Args:
            product (str): The product to track (e.g., 'RAINFOREST_RESIN' or 'KELP')
        """
        # Assign the Product Name to Instance Variable
        self.product = product  


    def update(self, state: TradingState) -> None:
        """
        Updates the market status with new data.

        Args:
            state (TradingState): The current state containing position and order depths.
        """
        # Update the Static State
        Status._state = state  

        # Update Real-time Positions for Each Product
        for product, posit in state.position.items():
            Status._realtime_position[product] = posit

        # Update Historical Order Depths for Each Product
        for product, orderdepth in state.order_depths.items():
            # Counter for Order Levels
            cnt = 1  

            # Process Sell Orders (asks)
            for prc, amt in sorted(orderdepth.sell_orders.items()):
                Status._hist_order_depths[product][f'askamt{cnt}'].append(amt)
                Status._hist_order_depths[product][f'askprc{cnt}'].append(prc)
                cnt += 1

                # Limit to Top 3 Levels
                if cnt == 4:  
                    break

            # Fill Remaining Ask Levels with NaN
            while cnt < 4:
                Status._hist_order_depths[product][f'askprc{cnt}'].append(np.nan)
                Status._hist_order_depths[product][f'askamt{cnt}'].append(np.nan)
                cnt += 1

            # Reset Counter for Bid Levels
            cnt = 1  


            # Process Buy Orders (bids)
            for prc, amt in sorted(orderdepth.buy_orders.items(), reverse=True):
                Status._hist_order_depths[product][f'bidprc{cnt}'].append(prc)
                Status._hist_order_depths[product][f'bidamt{cnt}'].append(amt)
                cnt += 1
                # Limit to Top 3 Levels
                if cnt == 4:  
                    break

            # Fill Remaining Bid Levels with NaN
            while cnt < 4:
                Status._hist_order_depths[product][f'bidprc{cnt}'].append(np.nan)
                Status._hist_order_depths[product][f'bidamt{cnt}'].append(np.nan)
                cnt += 1

        # Increment Data Update Counter
        Status._num_data += 1  


    def position_limit(self) -> int:
        """
        Returns the position limit for the tracked product.
        
        Returns:
            int: The position limit for the product.
        """
        return self._position_limit[self.product]


    def position(self) -> int:
        """
        Returns the current position for the tracked product.
        
        Returns:
            int: The current position of the product.
        """
        return int(Status._state.position.get(self.product, 0))


    def hist_order_depth(self, type: str, depth: int, size) -> np.ndarray:
        """
        Returns the historical order depth for the given type (bid/ask), depth, and size.

        Args:
            type (str): 'bid' or 'ask' to specify order type.
            depth (int): The order depth level (1, 2, or 3).
            size (int): The size of data to return.

        Returns:
            np.ndarray: The order depth data as a NumPy array.
        """
        return np.array(Status._hist_order_depths[self.product][f'{type}{depth}'][-size:], dtype=np.float32)


    def maxamt_bidprc(self) -> int:
        """
        Returns the bid price with the maximum amount.

        Returns:
            int: The price with the maximum bid amount.
        """
        # Initialise Variables to Track the Highest Bid Price and its Corresponding Amount
        prc_max_mat, max_amt = 0, 0

        # Iterate through Each Buy Order in the Order Depths for the Tracked Product
        for prc, amt in Status._state.order_depths[self.product].buy_orders.items():
            # If the Current Amount is Greater than the Maximum Found so far, Update the Max Values
            if amt > max_amt:
                max_amt = amt      # Update the Highest Amount
                prc_max_mat = prc  # Update the Corresponding Bid Price

        # Return the Price Associated with the Highest Amount
        return prc_max_mat


    def maxamt_askprc(self) -> int:
        """
        Returns the ask price with the minimum amount.

        Returns:
            int: The price with the minimum ask amount.
        """
        # Initialise Variables to Track the Lowest Ask Price and its Corresponding Amount
        prc_max_mat, max_amt = 0, 0

        # Iterate through each Sell Order in the Order Depths for the Tracked Product
        for prc, amt in Status._state.order_depths[self.product].sell_orders.items():
            # If the Current Amount is Less than the Lowest Found so far, Update the Max Values
            if amt < max_amt:
                max_amt = amt      # Update the Lowest Amount
                prc_max_mat = prc  # Update the Corresponding Ask Price

        # Return the Price Associated with the Lowest Amount
        return prc_max_mat


    def maxamt_midprc(self) -> float:
        """
        Returns the midpoint between the max bid price and max ask price.

        Returns:
            float: The midpoint price.
        """
        return (self.maxamt_bidprc() + self.maxamt_askprc()) / 2


    def _update_bids(self, prc, new_amt):
        """
        Updates the bid (buy) orders with the new amount at the given price.

        Args:
            prc (int): The price at which to update the bid.
            new_amt (int): The new amount to set for the bid.
        """
        if new_amt >= 0:
            Status._state.order_depths[self.product].buy_orders[prc] = new_amt


    def _update_asks(self, prc, new_amt):
        """
        Updates the ask (sell) orders with the new amount at the given price.

        Args:
            prc (int): The price at which to update the ask.
            new_amt (int): The new amount to set for the ask.
        """
        if new_amt <= 0:
            Status._state.order_depths[self.product].sell_orders[prc] = new_amt


    def _rt_position_update(self, new_position):
        """
        Updates the real-time position for the product, ensuring it doesn't exceed the position limit.

        Args:
            new_position (int): The new real-time position to set.

        Raises:
            ValueError: If the new position exceeds the product's position limit.
        """
        if abs(new_position) <= Status._position_limit[self.product]:
            Status._realtime_position[self.product] = new_position
        else:
            raise ValueError("New position exceeds limit")


    def asks(self) -> list[tuple[int, int]]:
        """
        Returns the list of ask orders (sell orders) for the product.

        Returns:
            list: A list of tuples (price, amount) representing the sell orders.
        """
        return list(Status._state.order_depths[self.product].sell_orders.items())


    def bids(self) -> list[tuple[int, int]]:
        """
        Returns the list of bid orders (buy orders) for the product.

        Returns:
            list: A list of tuples (price, amount) representing the buy orders.
        """
        return list(Status._state.order_depths[self.product].buy_orders.items())


    def rt_position_update(self, new_position: int) -> None:
        """
        Updates the real-time position for the product.

        Args:
            new_position (int): The new position to set.
        """
        self._rt_position_update(new_position)


    def rt_position(self) -> int:
        """
        Returns the current real-time position for the product.

        Returns:
            int: The current real-time position.
        """
        return Status._realtime_position[self.product]


    def update_asks(self, prc: int, new_amt: int) -> None:
        """
        Updates the ask (sell) order for the product.

        Args:
            prc (int): The price to update.
            new_amt (int): The new amount for the ask order.
        """
        self._update_asks(prc, new_amt)


    def update_bids(self, prc: int, new_amt: int) -> None:
        """
        Updates the bid (buy) order for the product.

        Args:
            prc (int): The price to update.
            new_amt (int): The new amount for the bid order.
        """
        self._update_bids(prc, new_amt)
    

    def possible_buy_amt(self) -> int:
        """Return possible buy amount. This function calculates 
        the possible amount of product that can be bought based 
        on the position limit and the current position.

        Returns:
            int: The possible buy amount, ensuring that the result does not exceed the 
            available position limit or the current position limit.
        """
        # Calculate the Available Buy Amount Considering the Real-time Position
        possible_buy_amount1 = self._position_limit[self.product] - self.rt_position()

        # Calculate the Available Buy Amount Considering the Historical Position
        possible_buy_amount2 = self._position_limit[self.product] - self.position()

        # Return the Smaller of the Two Possible Buy Amounts to Ensure No Position Limit is Exceeded
        return min(possible_buy_amount1, possible_buy_amount2)
            

    def possible_sell_amt(self) -> int:
        """Return possible sell amount. This function calculates 
        the possible amount of product that can be sold based 
        on the position limit and the current position.

        Returns:
            int: The possible sell amount, ensuring that the result does not exceed the 
                available position limit or the current position limit.
        """
        # Calculate the Available Sell Amount Considering the Real-time Position
        possible_sell_amount1 = self._position_limit[self.product] + self.rt_position()

        # Calculate the Available Sell Amount Considering the Historical Position
        possible_sell_amount2 = self._position_limit[self.product] + self.position()

        # Return the Smaller of the Two Possible Sell Amounts to Ensure no Position Limit is Exceeded
        return min(possible_sell_amount1, possible_sell_amount2)
    

    def best_bid(self) -> int:
        """Return best bid price and amount.

        This function returns the best (highest) bid price from the buy orders. 
        If there are no buy orders, it returns the best ask price minus 1, indicating that
        there is no current bid available.

        Returns:
            tuple[int, int]: A tuple containing the best bid price and amount.
        """
        # Fetch the Buy Orders from the Order Book for the Current Product
        buy_orders = self._state.order_depths[self.product].buy_orders

        # If there are Buy Orders, Return the Highest Bid Price (max of the keys)
        if len(buy_orders) > 0:
            return max(buy_orders.keys())
        
        # If No Buy Orders Exist, Return the Best Ask Price Minus 1
        else:
            return self.best_ask - 1


    def best_ask(self) -> int:
        """Return best ask price and amount.

        This function returns the best (lowest) ask price from the ask orders. 
        If there are no ask orders, it returns the best bid price plus 1, indicating that
        there is no current ask available.

        Returns:
            int: The best ask price.
        """
        # Fetch the Sell Orders from the Order Book for the Current Product
        sell_orders = self._state.order_depths[self.product].sell_orders

        # If there are Sell Orders, Return the Lowest Ask Price (min of the keys)
        if len(sell_orders) > 0:
            return min(sell_orders.keys())
        else:
            # If No Sell Orders Exist, Return the Best Bid Price Plus 1
            return self.best_bid + 1


# STRATEGY CLASS IMPLEMENTING ARBITRAGE AND MARKET MAKING STRATEGIES FOR TRADING BASED ON FAIR PRICE COMPARISON
class Strategy:
    def arb(state: Status, fair_price):
        """
        This method implements an arbitrage strategy that attempts to exploit price discrepancies 
        between the current market prices (bid/ask) and the fair price. It generates orders based on
        the price levels that provide opportunities for arbitrage.
        
        Parameters:
        - state: Current market state encapsulated in a Status object.
        - fair_price: The calculated fair price that the strategy compares against.
        
        Returns:
        - orders: List of generated buy and sell orders.
        """
        # List to Hold Generated Orders
        orders = [] 

        # Iterate Over Each Ask Price and its Corresponding Amount
        for ask_price, ask_amount in state.asks():
            # If the Ask Price is Lower than the Fair Price, Attempt to Buy
            if ask_price < fair_price:
                # Limit Buy Amount Based on Available Position
                buy_amount = min(-ask_amount, state.possible_buy_amt())  
                if buy_amount > 0:
                    # Create a Buy Order
                    orders.append(Order(state.product, int(ask_price), int(buy_amount)))  

                    # Update Real-time Position
                    state.rt_position_update(state.rt_position() + buy_amount)  

                    # Update Ask Depth After Placing the Order
                    state.update_asks(ask_price, -(-ask_amount - buy_amount))  


            # If the Ask Price is Equal to the Fair Price and the Position is Negative (sell orders to close), Buy
            elif ask_price == fair_price and state.rt_position() < 0:
                # Buy to Close Negative Position
                buy_amount = min(-ask_amount, -state.rt_position())  
                
                # Create Buy Order
                orders.append(Order(state.product, int(ask_price), int(buy_amount))) 

                # Update Position
                state.rt_position_update(state.rt_position() + buy_amount)  

                # Update Ask Depth After Placing the Order
                state.update_asks(ask_price, -(-ask_amount - buy_amount)) 


        # Iterate Over Each Bid Price and its Corresponding Amount
        for bid_price, bid_amount in state.bids():
            # If the Bid Price is Higher than the Fair Price, Attempt to Sell
            if bid_price > fair_price:
                # Limit Sell Amount Based on Available Position
                sell_amount = min(bid_amount, state.possible_sell_amt())  
                if sell_amount > 0:
                    # Create a Sell Order
                    orders.append(Order(state.product, int(bid_price), -int(sell_amount)))  

                    # Update Real-time Position
                    state.rt_position_update(state.rt_position() - sell_amount)  

                    # Update Bid Depth After Placing the Order
                    state.update_bids(bid_price, bid_amount - sell_amount)  


            # If the Bid Price Equals the Fair Price and the Position is Positive (buy orders to close), Sell
            elif bid_price == fair_price and state.rt_position() > 0:
                # Sell to Close Positive Position
                sell_amount = min(bid_amount, state.rt_position())  

                # Create Sell Order
                orders.append(Order(state.product, int(bid_price), -int(sell_amount)))  

                # Update Position
                state.rt_position_update(state.rt_position() - sell_amount) 

                # Update Bid Depth After Placing the Order
                state.update_bids(bid_price, bid_amount - sell_amount)  

        # Return the List of Generated Orders
        return orders


    def mm_ou(state: Status, fair_price, gamma=1e-9, order_amount=20):
        """
        This method implements a market-making strategy that adjusts the bid and ask prices 
        based on the fair price. The strategy uses a mathematical formula to calculate optimal 
        bid and ask prices and then generates the corresponding buy and sell orders.
        
        Parameters:
        - state: Current market state encapsulated in a Status object.
        - fair_price: The calculated fair price that the strategy adjusts bids and asks around.
        - gamma: A small constant used to adjust the price step.
        - order_amount: The amount of the product to buy/sell in each order.
        
        Returns:
        - orders: List of generated buy and sell orders.
        """
        # Calculate Current and Maximum Position as Fractions of the Order Amount
        q = state.rt_position() / order_amount
        Q = state.position_limit() / order_amount

        # Calculate Kappa Values for Bid and Ask Sides, which Adjust the Price Sensitivity
        kappa_b = 1 / max((fair_price - state.best_bid()) - 1, 1)
        kappa_a = 1 / max((state.best_ask() - fair_price) - 1, 1)
        
        # Define a Function to Calculate a Value Based on q and Q
        vfucn = lambda q, Q: float('-inf') if (q == Q + 1 or q == -(Q + 1)) else math.log(math.sin(((q + Q + 1) * math.pi) / (2 * Q + 2)))

        # Calculate Price Adjustments for Bid and Ask Prices
        delta_b = 1 / gamma * math.log(1 + gamma / kappa_b) - 1 / kappa_b * (vfucn(q + 1, Q) - vfucn(q, Q))
        delta_a = 1 / gamma * math.log(1 + gamma / kappa_a) + 1 / kappa_a * (vfucn(q, Q) - vfucn(q - 1, Q))

        # Cap delta_a to a maximum value to avoid infinity
        max_delta = 1e6  # Set a maximum delta value that is reasonable
        delta_b = min(delta_b, max_delta)
        delta_b = max(delta_b, -max_delta)
        delta_a = min(delta_a, max_delta)
        delta_a = max(delta_a, -max_delta)

        # Calculate the Optimal Bid and Ask Prices Based on the Fair Price and Adjustments
        p_b = round(fair_price - delta_b)        
        p_a = round(fair_price + delta_a)

        # Apply Constraints to the Calculated Bid and Ask Prices
        p_b = min(p_b, fair_price)                 # Ensure Buy Price Does Not Exceed Fair Price
        p_b = min(p_b, state.best_bid() + 1)       # Ensure Buy Price is Not Higher than the Best Bid
        p_b = max(p_b, state.maxamt_bidprc() + 1)  # Limit Market Order Arrival Beyond this Price

        p_a = max(p_a, fair_price)                 # Ensure Ask Price is Not Below Fair Price
        p_a = max(p_a, state.best_ask() - 1)       # Ensure Ask Price is Not Lower than the Best Ask
        p_a = min(p_a, state.maxamt_askprc() - 1)  # Limit Market Order Arrival Beyond this Price

        # Calculate Possible Buy and Sell Amounts Based on Position Limits
        buy_amount = min(order_amount, state.possible_buy_amt())
        sell_amount = min(order_amount, state.possible_sell_amt())

        # List to Hold Generated Orders
        orders = []

        # Create Buy Order if there is Enough Amount to Buy
        if buy_amount > 0:
            orders.append(Order(state.product, int(p_b), int(buy_amount)))
        
        # Create Sell Order if there is Enough Amount to Sell
        if sell_amount > 0:
            orders.append(Order(state.product, int(p_a), -int(sell_amount)))

        # Return the List of Generated Orders
        return orders



# CLASS CONTAINING STRATEGIES FOR EACH PRODUCT
class Trade:
    # Rainforest Resin Method
    def rainforestresin(state: Status) -> list[Order]:
        # Basic Strategy: place buy and sell orders near the midprice
        orders = []
        
        # Get Current Midprice
        current_price = state.maxamt_midprc()

        # Place Symmetric Orders with Fixed Quantity
        orders.extend(Strategy.arb(state=state, fair_price=current_price))   # Buy Order
        orders.extend(Strategy.mm_ou(state=state, fair_price=current_price, gamma=0.1, order_amount=20)) # Sell Order

        # Return the Result
        return orders


    # Kelp Strategy (Refined for Price Volatility)
    def kelp(state: Status) -> list[Order]:
        # Basic Strategy: place buy and sell orders near the midprice
        orders = []
        
        # Get Current Midprice
        current_price = state.maxamt_midprc()

        # Place Symmetric Orders with Fixed Quantity
        orders.extend(Strategy.arb(state=state, fair_price=current_price))   # Buy Order
        orders.extend(Strategy.mm_ou(state=state, fair_price=current_price, gamma=0.1, order_amount=20)) # Sell Order

        # Return the Result
        return orders


    # Squid Strategy (Moving Average)
    def squid(state: Status) -> list[Order]:
        # Basic Strategy: place buy and sell orders near the midprice
        orders = []
        
        # Get Current Midprice
        current_price = state.maxamt_midprc()

        # Place Symmetric Orders with Fixed Quantity
        orders.extend(Strategy.arb(state=state, fair_price=current_price))   # Buy Order
        orders.extend(Strategy.mm_ou(state=state, fair_price=current_price, gamma=0.1, order_amount=20)) # Sell Order

        # Return the Result
        return orders



# MAIN ENTRYPOINT FOR THE TRADING AGENT
class Trader:
    # Create One Status Object Per Product
    state_RAINFOREST_RESIN = Status('RAINFOREST_RESIN')
    state_KELP = Status('KELP')
    state_SQUID = Status('SQUID_INK')

    # The Main Run Function
    def run(self, state: TradingState) -> tuple[dict[Symbol, list[Order]], int, str]:
        # Update Internal Class State with Current Round's Info
        Status.update(Status, state)

        # Intalise Result Dictionary
        result = {} 

        # Use the Defined Strategies for Each Product
        result["RAINFOREST_RESIN"] = Trade.rainforestresin(self.state_RAINFOREST_RESIN)
        result["KELP"] = Trade.kelp(self.state_KELP)
        result["SQUID_INK"] = Trade.squid(self.state_SQUID)

        # Return Orders, Conversions (0 = no request), and a Log String
        traderData = "SAMPLE"  # Placeholder string, this will be the data provided to the next execution
        conversions = 1        # Indicates that a conversion was made (1 = conversion request, 0 = no request)
        return result, conversions, traderData