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
    _state = None
    _num_data = 0

    _position_limit = {
        "RAINFOREST_RESIN": 50,
        "KELP": 50,
    }

    _realtime_position = {key: 0 for key in _position_limit.keys()}

    _hist_order_depths = {
        product: {
            'bidprc1': [], 'bidamt1': [],
            'bidprc2': [], 'bidamt2': [],
            'bidprc3': [], 'bidamt3': [],
            'askprc1': [], 'askamt1': [],
            'askprc2': [], 'askamt2': [],
            'askprc3': [], 'askamt3': [],
        } for product in _position_limit.keys()
    }

    def __init__(self, product: str) -> None:
        self.product = product

    def update(self, state: TradingState) -> None:
        Status._state = state

        for product, posit in state.position.items():
            Status._realtime_position[product] = posit

        for product, orderdepth in state.order_depths.items():
            cnt = 1
            for prc, amt in sorted(orderdepth.sell_orders.items()):
                Status._hist_order_depths[product][f'askamt{cnt}'].append(amt)
                Status._hist_order_depths[product][f'askprc{cnt}'].append(prc)
                cnt += 1
                if cnt == 4:
                    break
            while cnt < 4:
                Status._hist_order_depths[product][f'askprc{cnt}'].append(np.nan)
                Status._hist_order_depths[product][f'askamt{cnt}'].append(np.nan)
                cnt += 1

            cnt = 1
            for prc, amt in sorted(orderdepth.buy_orders.items(), reverse=True):
                Status._hist_order_depths[product][f'bidprc{cnt}'].append(prc)
                Status._hist_order_depths[product][f'bidamt{cnt}'].append(amt)
                cnt += 1
                if cnt == 4:
                    break
            while cnt < 4:
                Status._hist_order_depths[product][f'bidprc{cnt}'].append(np.nan)
                Status._hist_order_depths[product][f'bidamt{cnt}'].append(np.nan)
                cnt += 1

        Status._num_data += 1
    
    def position_limit(self) -> int:
        return self._position_limit[self.product]

    def position(self) -> int:
        return int(Status._state.position.get(self.product, 0))

    def hist_order_depth(self, type: str, depth: int, size) -> np.ndarray:
        return np.array(Status._hist_order_depths[self.product][f'{type}{depth}'][-size:], dtype=np.float32)

    def maxamt_bidprc(self) -> int:
        prc_max_mat, max_amt = 0, 0
        for prc, amt in Status._state.order_depths[self.product].buy_orders.items():
            if amt > max_amt:
                max_amt = amt
                prc_max_mat = prc
        return prc_max_mat

    def maxamt_askprc(self) -> int:
        prc_max_mat, max_amt = 0, 0
        for prc, amt in Status._state.order_depths[self.product].sell_orders.items():
            if amt < max_amt:
                max_amt = amt
                prc_max_mat = prc
        return prc_max_mat

    def maxamt_midprc(self) -> float:
        return (self.maxamt_bidprc() + self.maxamt_askprc()) / 2

    def _update_bids(self, prc, new_amt):
        if new_amt >= 0:
            Status._state.order_depths[self.product].buy_orders[prc] = new_amt

    def _update_asks(self, prc, new_amt):
        if new_amt <= 0:
            Status._state.order_depths[self.product].sell_orders[prc] = new_amt

    def _rt_position_update(self, new_position):
        if abs(new_position) <= Status._position_limit[self.product]:
            Status._realtime_position[self.product] = new_position
        else:
            raise ValueError("New position exceeds limit")

    def asks(self) -> list[tuple[int, int]]:
        return list(Status._state.order_depths[self.product].sell_orders.items())

    def bids(self) -> list[tuple[int, int]]:
        return list(Status._state.order_depths[self.product].buy_orders.items())

    def rt_position_update(self, new_position: int) -> None:
        self._rt_position_update(new_position)

    def rt_position(self) -> int:
        return Status._realtime_position[self.product]

    def update_asks(self, prc: int, new_amt: int) -> None:
        self._update_asks(prc, new_amt)

    def update_bids(self, prc: int, new_amt: int) -> None:
        self._update_bids(prc, new_amt)

    def possible_buy_amt(self) -> int:
        return min(Status._position_limit[self.product] - self.rt_position(), 
                   Status._position_limit[self.product] - self.position())

    def possible_sell_amt(self) -> int:
        return min(Status._position_limit[self.product] + self.rt_position(), 
                   Status._position_limit[self.product] + self.position())

    def best_bid(self) -> int:
        buy_orders = self._state.order_depths[self.product].buy_orders
        if len(buy_orders) > 0:
            return max(buy_orders.keys())
        else:
            return self.best_ask - 1

    def best_ask(self) -> int:
        sell_orders = self._state.order_depths[self.product].sell_orders
        if len(sell_orders) > 0:
            return min(sell_orders.keys())
        else:
            return self.best_bid + 1



class Strategy:

    def arb(state: Status, fair_price):
        orders = []

        for ask_price, ask_amount in state.asks():
            if ask_price < fair_price:
                buy_amount = min(-ask_amount, state.possible_buy_amt())
                if buy_amount > 0:
                    orders.append(Order(state.product, int(ask_price), int(buy_amount)))
                    state.rt_position_update(state.rt_position() + buy_amount)
                    state.update_asks(ask_price, -(-ask_amount - buy_amount))

            elif ask_price == fair_price and state.rt_position() < 0:
                buy_amount = min(-ask_amount, -state.rt_position())
                orders.append(Order(state.product, int(ask_price), int(buy_amount)))
                state.rt_position_update(state.rt_position() + buy_amount)
                state.update_asks(ask_price, -(-ask_amount - buy_amount))

        for bid_price, bid_amount in state.bids():
            if bid_price > fair_price:
                sell_amount = min(bid_amount, state.possible_sell_amt())
                if sell_amount > 0:
                    orders.append(Order(state.product, int(bid_price), -int(sell_amount)))
                    state.rt_position_update(state.rt_position() - sell_amount)
                    state.update_bids(bid_price, bid_amount - sell_amount)

            elif bid_price == fair_price and state.rt_position() > 0:
                sell_amount = min(bid_amount, state.rt_position())
                orders.append(Order(state.product, int(bid_price), -int(sell_amount)))
                state.rt_position_update(state.rt_position() - sell_amount)
                state.update_bids(bid_price, bid_amount - sell_amount)

        return orders

    def mm_ou(state: Status, fair_price, gamma=1e-9, order_amount=20):
        q = state.rt_position() / order_amount
        Q = state.position_limit() / order_amount

        kappa_b = 1 / max((fair_price - state.best_bid()) - 1, 1)
        kappa_a = 1 / max((state.best_ask() - fair_price) - 1, 1)
            
        vfucn = lambda q,Q: float('-inf') if (q==Q+1 or q==-(Q+1)) else math.log(math.sin(((q+Q+1)*math.pi)/(2*Q+2)))

        delta_b = 1 / gamma * math.log(1 + gamma / kappa_b) - 1 / kappa_b * (vfucn(q + 1, Q) - vfucn(q, Q))
        delta_a = 1 / gamma * math.log(1 + gamma / kappa_a) + 1 / kappa_a * (vfucn(q, Q) - vfucn(q - 1, Q))

        p_b = round(fair_price - delta_b)        
        p_a = round(fair_price + delta_a)

        p_b = min(p_b, fair_price) # Set the buy price to be no higher than the fair price to avoid losses
        p_b = min(p_b, state.best_bid() + 1) # Place the buy order as close as possible to the best bid price
        p_b = max(p_b, state.maxamt_bidprc() + 1) # No market order arrival beyond this price

        p_a = max(p_a, fair_price)
        p_a = max(p_a, state.best_ask() - 1)
        p_a = min(p_a, state.maxamt_askprc() - 1)

        buy_amount = min(order_amount, state.possible_buy_amt())
        sell_amount = min(order_amount, state.possible_sell_amt())

        orders = []
        if buy_amount > 0:
            orders.append(Order(state.product, int(p_b), int(buy_amount)))
        if sell_amount > 0:
            orders.append(Order(state.product, int(p_a), -int(sell_amount)))
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
        Status.update(Status, state)

        # Intalise Result Dictionary
        result = {} 

        # Use the Defined Strategies for Each Product
        result["RAINFOREST_RESIN"] = Trade.rainforestresin(self.state_RAINFOREST_RESIN)
        result["KELP"] = Trade.kelp(self.state_KELP)

        # Return Orders, Conversions (0 = no request), and a Log String
        traderData = "SAMPLE"  # Placeholder string, this will be the data provided to the next execution
        conversions = 1        # Indicates that a conversion was made (1 = conversion request, 0 = no request)
        return result, conversions, traderData