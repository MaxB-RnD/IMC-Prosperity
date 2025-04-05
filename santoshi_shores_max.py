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
    # Will Hold the Most Recent Trading State
    _state = None  

    # Tracks How mMany Updates We’ve Seen
    _num_data = 0  

    # Set Product Position Limits
    _position_limit = {
        "RAINFOREST_RESIN": 50,
        "KELP": 50,
    }


    # Initialise Real-Time Positions to Zero
    _realtime_position = {key: 0 for key in _position_limit.keys()}


    # Initialise Historical Order Depth Dictionaries for Each Product
    _hist_order_depths = {
        product: {
            'bidprc1': [], 'bidamt1': [],
            'bidprc2': [], 'bidamt2': [],
            'bidprc3': [], 'bidamt3': [],
            'askprc1': [], 'askamt1': [],
            'askprc2': [], 'askamt2': [],
            'askprc3': [], 'askamt3': [],
        } 
        for product in _position_limit.keys()
    }


    # Class Constructor
    def __init__(self, product: str) -> None:
        # Set the Product this Instance Will Track
        self.product = product 


    # The Main Method for the Satus Class
    def cls_update(cls, state: TradingState) -> None:
        cls._state = state  # save the latest state

        # Update Current Positions
        for product, posit in state.position.items():
            cls._realtime_position[product] = posit

        # Update Order Book History for Each Product
        for product, orderdepth in state.order_depths.items():
            # Update Sell Orders (asks) Sorted from Low to High Price
            cnt = 1
            for prc, amt in sorted(orderdepth.sell_orders.items(), reverse=False):
                cls._hist_order_depths[product][f'askamt{cnt}'].append(amt)
                cls._hist_order_depths[product][f'askprc{cnt}'].append(prc)
                cnt += 1
                if cnt == 4:
                    break
            while cnt < 4:
                cls._hist_order_depths[product][f'askprc{cnt}'].append(np.nan)
                cls._hist_order_depths[product][f'askamt{cnt}'].append(np.nan)
                cnt += 1

            # Update Buy Orders (bids) Sorted from High to Low Price
            cnt = 1
            for prc, amt in sorted(orderdepth.buy_orders.items(), reverse=True):
                cls._hist_order_depths[product][f'bidprc{cnt}'].append(prc)
                cls._hist_order_depths[product][f'bidamt{cnt}'].append(amt)
                cnt += 1
                if cnt == 4:
                    break
            while cnt < 4:
                cls._hist_order_depths[product][f'bidprc{cnt}'].append(np.nan)
                cls._hist_order_depths[product][f'bidamt{cnt}'].append(np.nan)
                cnt += 1

        # Increment the Number of Rounds 
        cls._num_data += 1


    # Keeps Track of the Order Depth
    def hist_order_depth(self, type: str, depth: int, size) -> np.ndarray:
        # Returns the Recent History of Bids or Asks for a Given Depth Level
        return np.array(self._hist_order_depths[self.product][f'{type}{depth}'][-size:], dtype=np.float32)


    # Returns the Price Level with the Highest Buy Volume
    def maxamt_bidprc(self) -> int:
        # Initialise Variables to Track the Price and the Largest Amount
        prc_max_mat, max_amt = 0, 0

        # Iterate through all Buy Orders for this Product
        for prc, amt in self._state.order_depths[self.product].buy_orders.items():
            # Check if this amount is greater than the current max (i.e., higher buy volume)
            if amt > max_amt:
                max_amt = amt      # update the max buy volume
                prc_max_mat = prc  # update the corresponding price level

        # Return the Price Level that had the Highest Buy Volume
        return prc_max_mat

    
    # Returns the Price Level with the Highest Sell Volume (most negative amount)
    def maxamt_askprc(self) -> int:
        # Initialise Variables to Track the Price and the Most Negative Amount (i.e., highest volume sell)
        prc_max_mat, max_amt = 0, 0

        # Iterate through all Sell Orders for this Product
        for prc, amt in self._state.order_depths[self.product].sell_orders.items():
            # Check if this amount is more negative (larger sell volume) than the current max
            if amt < max_amt:
                max_amt = amt      # update the most negative amount
                prc_max_mat = prc  # update the corresponding price level

        # Return the Price Level that had the Largest (most negative) Sell Volume
        return prc_max_mat


    # Calculates a Midprice Using the Max-Volume Bid & Ask Prices
    def maxam_midprc(self) -> float:
        return (self.maxamt_bidprc() + self.maxamt_askprc()) / 2



# CLASS CONTAINING STRATEGIES FOR EACH PRODUCT
class Trade:
    # Rainforest Resin Method
    def rainforestresin(state: Status) -> list[Order]:
        # Basic Strategy: place buy and sell orders near the midprice
        orders = []
        
        # Get Current Midprice
        midprice = state.maxam_midprc()  

        # Buy Just Below Midprice
        fair_bid = int(midprice) - 1 

        # Sell Just Above Midprice  
        fair_ask = int(midprice) + 1   

        # Place Symmetric Orders with Fixed Quantity
        orders.append(Order(state.product, fair_bid, 5))   # Buy Order
        orders.append(Order(state.product, fair_ask, -5))  # Sell Order

        # Return the Result
        return orders


    # Kelp Method
    def kelp(state: Status) -> list[Order]:
        # For Now, use the Same Strategy as Rainforest Resin
        return Trade.rainforestresin(state)



# MAIN ENTRYPOINT FOR THE TRADING AGENT
class Trader:
    # Create One Status Object Per Product
    state_RAINFOREST_RESIN = Status('RAINFOREST_RESIN')
    state_KELP = Status('KELP')


    # The Main Run Function
    def run(self, state: TradingState) -> tuple[dict[Symbol, list[Order]], int, str]:
        # Update Internal Class State with Current Round's Info
        Status.cls_update(Status, state)

        # Intalise Result Dictionary
        result = {} 

        # Use the Defined Strategies for Each Product
        result["RAINFOREST_RESIN"] = Trade.rainforestresin(self.state_RAINFOREST_RESIN)
        result["KELP"] = Trade.kelp(self.state_KELP)

        # Return Orders, Conversions (0 = no request), and a Log String
        traderData = "SAMPLE"  # Placeholder string, this will be the data provided to the next execution
        conversions = 1        # Indicates that a conversion was made (1 = conversion request, 0 = no request)
        return result, conversions, traderData