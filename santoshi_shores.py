import json
import numpy as np
import math
from datamodel import *
from typing import Any

from statistics import NormalDist

class Status:
    _position_limit = {
        "RAINFOREST_RESIN": 50,
        "KELP": 50,
    }

    
    _realtime_position = {key:0 for key in _position_limit.keys()}

    _hist_order_depths = {
        product:{
            'bidprc1': [],
            'bidamt1': [],
            'bidprc2': [],
            'bidamt2': [],
            'bidprc3': [],
            'bidamt3': [],
            'askprc1': [],
            'askamt1': [],
            'askprc2': [],
            'askamt2': [],
            'askprc3': [],
            'askamt3': [],
        } for product in _position_limit.keys()
    }
    

    _state = None
    _num_data = 0

    def __init__(self,product:str) -> None:
        self.product = product

    @classmethod
    def cls_update(cls, state:TradingState)-> None:
        cls._state = state

        # Update realtime position
        for product, posit in state.position.items():
            cls._realtime_position[product] = posit
        # Update historical order_depths
        for product, orderdepth in state.order_depths.items():
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
        cls._num_data += 1

    def hist_order_depth(self, type: str, depth: int, size) -> np.ndarray:
        """Return historical order depth.

        Args:
            type (str): 'bidprc' or 'bidamt' or 'askprc' or 'askamt'
            depth (int): depth, 1 or 2 or 3
            size (int): size of data

        Returns:
            np.ndarray: historical order depth for given type and depth

        """
        return  np.array(self._hist_order_depths[self.product][f'{type}{depth}'][-size:], dtype=np.float32)

    @property
    def maxamt_bidprc(self) -> int:
        """Return price of bid order with maximum amount.
        
        Returns:
            int: price of bid order with maximum amount

        """
        prc_max_mat, max_amt = 0,0
        for prc, amt in self._state.order_depths[self.product].buy_orders.items():
            if amt > max_amt:
                max_amt = amt
                prc_max_mat = prc

        return prc_max_mat
    
    @property
    def maxamt_askprc(self) -> int:
        """Return price of ask order with maximum amount.

        Returns:
            int: price of ask order with maximum amount
        
        """
        prc_max_mat, max_amt = 0,0
        for prc, amt in self._state.order_depths[self.product].sell_orders.items():
            if amt < max_amt:
                max_amt = amt
                prc_max_mat = prc

        return prc_max_mat

    @property
    def maxam_midprc(self)->float:
        return(self.maxamt_bidprc + self.maxam_askprc)/2



class Trade:
    @staticmethod
    def rainforesresin(state: Status) -> list[Order]:
    




class Trader: 
    state_RAINFOREST_RESIN = Status('RAINFOREST_RESIN')
    state_KELP = Status('KELP')

    def run(self, state: TradingState) -> tuple[dict[Symbol, list[Order]], int, str]:
        Status.cls_update(state)

        result = {}

        # Round 0
        result["RAINFOREST_RESIN"] = Trade.rainforestresin(self.state_RAINFOREST_RESIN)
        result["KELP"] = Trade.kelp(self.state_RAINFOREST_RESIN)

    


        
