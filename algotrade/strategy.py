# -*- coding: utf-8 -*-

# ライブラリのインポート
from abc import ABC

import pandas as pd
import numpy as np
from backtesting import Strategy
from backtesting.lib import crossover
from algotrade.indicator import highest_in_the_past, lowest_in_the_past, sma


class CounterTrend(Strategy, ABC):
    """カウンタートレンド戦略のクラス
    """
    # Define the two lags as *class variables*
    # for later optimization
    n_past = 35
    atr_periods = 30
    n_atr = 2
    n_day = 40  # n_dayは変えてもあまり結果がかわらない

    __n_atr = 3
    __atr = None

    def __init__(self, broker, data):
        super().__init__(broker, data)
        self.highest_in_range = self.I(highest_in_the_past, self.data.High, self.n_past)  # Max
        self.lowest_in_range = self.I(lowest_in_the_past, self.data.Low, self.n_past)  # Min
        self.set_atr_periods(self.atr_periods)
        self.set_trailing_sl(self.n_atr)

    def set_atr_periods(self, atr_periods: int = 100):
        """ATRを計算するときのlookback periodを設定する関数

        args:
            atr_periods(int): lookback period. The default value of 100 ensures a _stable_ ATR.

        """
        h, l, c_prev = self.data.High, self.data.Low, pd.Series(self.data.Close).shift(1)
        tr = np.max([h - l, (c_prev - h).abs(), (c_prev - l).abs()], axis=0)
        atr = pd.Series(tr).rolling(atr_periods).mean().bfill().values
        self.__atr = atr

    def set_trailing_sl(self, n_atr: float = 2):
        """損切りのATRの倍率を設定する関数

        Sets the future trailing stop-loss as some multiple (`n_atr`)
        average true bar ranges away from the current price.

        args:
            n_atr(float): 損切りのATRの倍率

        """
        self.__n_atr = n_atr

    def next(self):
        """トレード戦略の関数

        Sets the future trailing stop-loss as some multiple (`n_atr`)
        average true bar ranges away from the current price.

        """
        # ATRに基づいて損切り
        if self.__n_atr and self.position:
            if self.position.is_long:
                self.orders.set_sl(self.data.Close[-1] - self.__atr[-1] * self.__n_atr)
            else:
                self.orders.set_sl(self.data.Close[-1] + self.__atr[-1] * self.__n_atr)

        # 最高値を更新したら買い、最低を更新したら売り
        if crossover(self.data.High, self.highest_in_range):
            self.buy()
        elif crossover(self.lowest_in_range, self.data.Low):
            self.sell()

        # 最高値を更新したあと、戻したら売り、最低を更新したあと、戻したら売り
        if crossover(self.highest_in_range, self.data.High):
            self.sell()
        elif crossover(self.data.Low, self.lowest_in_range):
            self.buy()

        # 経過日数に基づいてポジションのクローズ
        if self.position and (self.position.pl <= 0):
            if (self.data.index[0] - self.position.open_time).days > self.n_day:
                self.position.close()


class SmaCross(Strategy, ABC):
    """smaの交差を使った戦略のクラス
    """
    # Define the two MA lags as *class variables*
    # for later optimization
    n1 = 10
    n2 = 20

    def __init__(self, broker, data):
        super().__init__(broker, data)
        self.sma_short = self.I(sma, self.data.Close, self.n1)  # 短期の移動平均線
        self.sma_long = self.I(sma, self.data.Close, self.n2)  # 長期の移動平均線

    def next(self):
        """トレード戦略の関数

        sma_shortがsma_longを上回ったら、買い注文
        sma_shortがsma_longを下回ったら、売り注文

        """
        if crossover(self.sma_short, self.sma_long):
            self.buy()
        elif crossover(self.sma_long, self.sma_short):
            self.sell()
