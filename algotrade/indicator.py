# -*- coding: utf-8 -*-
import pandas as pd


def sma(values: pd.Series, n: int) -> pd.Series:
    """移動平均を計算する関数

    array形式のvaluesを受け取り、ウィンドウ幅nの移動平均を計算する

    args:
        values(np.array): 移動平均を算出する対象. pd.Seriesでもいけると思う
        n(int): 移動平均のウィンドウ幅

    Returns:
        pd.Series: ウィンドウ幅nでのvaluesの移動平均

    Note:
        ウィンドウnは、各ステップの前側のnをとる

    """
    return values.rolling(n).mean()


def highest_in_the_past(values: pd.Series, n: int) -> pd.Series:
    """過去の特定期間内での最大値を出力する関数

    array形式のvaluesを受け取り、ウィンドウ幅n内での最大値を出力する関数

    args:
        values(pd.Series): 移動平均を算出する対象. pd.Seriesでもいけると思う
        n(int): 最大値を計算するウィンドウ幅

    Returns:
        pd.Series: ウィンドウ幅nでのvaluesの最大値

    Note:
        ウィンドウnは、各ステップの前側のnをとる

    """
    return values.shift(1).rolling(n).max()


def lowest_in_the_past(values: pd.Series, n: int) -> pd.Series:
    """過去の特定期間内での最小値を出力する関数

    array形式のvaluesを受け取り、ウィンドウ幅n内での最大値を出力する関数

    args:
        values(pd.Series): 移動平均を算出する対象
        n(int): 最大値を計算するウィンドウ幅

    Returns:
        pd.Series: ウィンドウ幅nでのvaluesの最小値

    Note:
        ウィンドウnは、各ステップの前側のnをとる

    """
    return values.shift(1).rolling(n).min()


def sigma(values: pd.Series, n: int = 20, n_sigma: int = 1) -> pd.Series:
    """ ボリンジャーバンドのσを出力する関数

    移動標準偏差(ボリンジャーバンドのσ)を出力する関数

    args:
        values(pd.Series): 移動標準偏差を算出する対象
        n(int): 移動標準偏差を計算するウィンドウ幅. デフォルトは20
        n_sigma(int): sigmaの倍率. デフォルトは1

    Returns:
        pd.Series: ウィンドウ幅nでのvaluesの移動標準偏差

    Note:
        ウィンドウnは、各ステップの前側のnをとる

    """
    return n_sigma * values.rolling(n).std()


def rsi(value: pd.Series, n: int = 20) -> pd.Series:
    """相対力指数(Relative strength index)を計算する関数

    args:
        values(pd.Series): 相対力指数を算出する対象
        n(int): 相対力指数を計算するウィンドウ幅. デフォルトは20

    Returns:
        pd.Series: ウィンドウ幅nでのvaluesの相対力指数

    Note:
        ウィンドウnは、各ステップの前側のnをとる
        Approximate; good enough

    """
    gain = pd.Series(value).diff()
    loss = gain.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    rs = gain.ewm(n).mean() / loss.abs().ewm(n).mean()
    return 100 - 100 / (1 + rs)
