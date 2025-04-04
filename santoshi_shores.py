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

    _state = None
    _num_data = 0

    def __init__(self,product:str) -> None:
        self.product = product

    @classmethod
    def cls_update(cls, state:TradingState)-> None:
        cls._state = state






class Trader: 
    state_RAINFOREST_RESIN = Status('RAINFOREST_RESIN')
    state_KELP = Status('KELP')

    def run(self, state: TradingState) -> tuple[dict[Symbol, list[Order]], int, str]:
        Status.cls_update(state)

        result = {}

        # Round 0
        result["RAINFOREST_RESIN"] = Trade.rainforestresin(self.state_RAINFOREST_RESIN)
        result["KELP"] = Trade.kelp(self.state_RAINFOREST_RESIN)

    


        
