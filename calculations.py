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
    current_position = 0
    prices = df[constants.CLOSE_COLUMN]
    longs = np.full(prices.shape, False)
    shorts = np.full(prices.shape, False)
    profits = np.zeros_like(prices)
    positions = np.zeros_like(prices)
    stop_loss = np.full(prices.shape, False)
    open_price = -1

    for i in range(constants.BOLLINGER_PERIOD, len(prices)):
        profits[i] = (prices[i] - prices[i-1]) * current_position * constants.NO_OF_SHARES

        if (current_position == 1 and prices[i] <= open_price * (1 - constants.LONG_STOP_LOSS_FACTOR)) \
                or (current_position == -1 and prices[i] >= open_price * (1 + constants.SHORT_STOP_LOSS_FACTOR)):
            current_position = 0
            stop_loss[i] = True
            open_price = -1
            profits[i] -= constants.TRADING_FEE
            continue

        if prices[i] <= lower_band[i] and current_position != 1:
            current_position = 1
            longs[i] = True
            open_price = prices[i]
        elif prices[i] >= upper_band[i] and current_position != -1:
            current_position = -1
            shorts[i] = True
            open_price = prices[i]
        if longs[i] or shorts[i]:
            profits[i] -= constants.TRADING_FEE * 2
        positions[i] = current_position

    return longs, shorts, profits, stop_loss


def annualised_sharpe(returns, period=252):
    return np.sqrt(period) * returns.mean() / returns.std()
