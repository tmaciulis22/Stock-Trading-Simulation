import constants
import numpy as np


def calculate_bollinger_band(df):
    moving_avg = np.round(df[constants.CLOSE_COLUMN].rolling(window=constants.BOLLINGER_PERIOD).mean(), 2)

    std = np.round(df[constants.CLOSE_COLUMN].rolling(window=constants.BOLLINGER_PERIOD).std(), 2)
    multiplied_std = np.multiply(std, constants.BOLLINGER_MULTIPLIER)

    upper_band = np.round(np.add(moving_avg, multiplied_std), 2)
    lower_band = np.round(np.subtract(moving_avg, multiplied_std), 2)

    return upper_band, moving_avg, lower_band


def simulate_strategy(df, upper_band, lower_band):
    should_sell = False
    prices = df[constants.CLOSE_COLUMN]
    buys = np.full(prices.shape, False)
    sells = np.full(prices.shape, False)
    stop_loss = np.full(prices.shape, False)
    profits = np.zeros_like(prices)
    open_price = -1

    for i in range(constants.BOLLINGER_PERIOD, len(df.index)):
        if should_sell:
            total_price = prices[i] * constants.NO_OF_SHARES
            total_prev_price = prices[i-1] * constants.NO_OF_SHARES
            profits[i] = \
                (total_price - total_price * constants.TRADING_FEE) \
                - (total_prev_price - total_prev_price * constants.TRADING_FEE)
        if prices[i] <= lower_band[i] and not should_sell:
            should_sell = True
            buys[i] = True
            open_price = prices[i]
        elif prices[i] >= upper_band[i] and should_sell:
            should_sell = False
            sells[i] = True
        elif prices[i] <= open_price * (1 - constants.STOP_LOSS_FACTOR):
            should_sell = False
            stop_loss[i] = True
            open_price = -1

    return buys, sells, stop_loss, profits
