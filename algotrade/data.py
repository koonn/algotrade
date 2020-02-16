# -*- coding: utf-8 -*-
import pandas as pd
from pandas.core import resample


def read_fx(filepath: str, fill_time: bool = True) -> pd.DataFrame:
    """histdataから入手したFX用のデータを、backtradingで使える形で読み込む関数
    """
    # 欠損timeを埋める関数
    def fill_missing_time(missing_df):
        # データセット期間中の欠損timeを埋める
        time_index = pd.date_range(missing_df.index.min(), missing_df.index.max(), freq='1min')
        # インデックスを振り直し、欠損を直前の値で埋める
        filled_df = missing_df.reindex(index=time_index).ffill()
        return filled_df

    df = pd.read_table(filepath, sep=';', header=None, index_col=0, parse_dates=True)
    # カラム名を大文字に直す
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    df.index.name = 'Time'

    # fill_timeがTrueなら欠損を埋める
    if fill_time:
        df = fill_missing_time(df)

    return df


def ohlc2(self: resample.DatetimeIndexResampler) -> pd.DataFrame:
    """時系列データのリサンプリングを行なった後に、OHLCを新しい時間軸に対して再度計算するための関数

    時系列データのリサンプリングを行なった後に、OHLCを新しい時間軸に対して再度計算するための関数
    `pd.DataFrame.resample(<TimeFrame>).ohlc2()`というメソッドとして使うことを想定

    """
    if all(i in ['Open', 'High', 'Low', 'Close'] for i in self.asfreq().columns):  # データに出来高が含まれないとき
        return self.agg({'Open': 'first',
                         'High': 'max',
                         'Low': 'min',
                         'Close': 'last'})
    elif all(i in ['Open', 'High', 'Low', 'Close', 'Volume'] for i in self.asfreq().columns):  # データに出来高が含まれるとき
        return self.agg({'Open': 'first',
                         'High': 'max',
                         'Low': 'min',
                         'Close': 'last',
                         'Volume': 'sum'})
    else:  # `Open High Low Close (Volume)`の列名で構成されていない場合はエラー
        raise KeyError("columns must have ['Open', 'High', 'Low', 'Close'(, 'Volume')]")


# pd.resampleのクラスにohlc2メソッドを追加
resample.DatetimeIndexResampler.ohlc2 = ohlc2
