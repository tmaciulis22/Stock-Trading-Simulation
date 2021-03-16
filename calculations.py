import constants
import numpy as np


def calculate_bollinger_band(df, period=constants.BOLLINGER_PERIOD, multiplier=constants.BOLLINGER_MULTIPLIER):
    moving_avg = np.round(df[constants.CLOSE_COLUMN].rolling(window=period).mean(), 2)

    std = np.round(df[constants.CLOSE_COLUMN].rolling(window=period).std(), 2)
    multiplied_std = np.multiply(std, multiplier)

    upper_band = np.round(np.add(moving_avg, multiplied_std), 2)
    lower_band = np.round(np.subtract(moving_avg, multiplied_std), 2)

    return upper_band, moving_avg, lower_band


def simulate_strategy(df, upper_band, lower_band, period=constants.BOLLINGER_PERIOD):
    current_position = 0
    prices = df[constants.CLOSE_COLUMN]
    longs = np.full(prices.shape, False)
    shorts = np.full(prices.shape, False)
    profits = np.zeros_like(prices)
    positions = np.zeros_like(prices)
    stop_loss = np.full(prices.shape, False)
    open_price = -1

    for i in range(period, len(prices)):
        profits[i] = (prices[i] - prices[i - 1]) * current_position * constants.NO_OF_SHARES

        if (current_position == 1 and prices[i] <= open_price * (1 - constants.LONG_STOP_LOSS_FACTOR)) \
                or (current_position == -1 and prices[i] >= open_price * (1 + constants.SHORT_STOP_LOSS_FACTOR)):
            current_position = 0
            stop_loss[i] = True
            open_price = -1
            profits[i] -= constants.TRADING_FEE
            continue

        if prices[i] <= (lower_band[i]) and current_position != 1:
            current_position = 1
            longs[i] = True
            open_price = prices[i]
        elif prices[i] >= (upper_band[i]) and current_position != -1:
            current_position = -1
            shorts[i] = True
            open_price = prices[i]
        if longs[i] or shorts[i]:
            profits[i] -= constants.TRADING_FEE * 2
        positions[i] = current_position

    sharpe_ratio = annualised_sharpe(profits)

    return longs, shorts, profits, stop_loss, sharpe_ratio


def find_optimized_strategy(df):
    max_sharpe_ratio = 0
    upper_band, middle_band, lower_band = None, None, None
    longs, shorts, profits, stop_loss = None, None, None, None
    optimized_period, optimized_multiplier = None, None

    for period in range(1, 40, 2):
        for multiplier in range(1, 5):
            temp_upper_band, temp_middle_ban, temp_lower_band = calculate_bollinger_band(df, period, multiplier)
            temp_longs, temp_shorts, temp_profits, temp_stop_loss, temp_sharpe_ratio = simulate_strategy(
                df,
                temp_upper_band,
                temp_lower_band,
                period
            )
            if temp_sharpe_ratio > max_sharpe_ratio:
                max_sharpe_ratio = temp_sharpe_ratio
                longs, shorts, profits, stop_loss = temp_longs, temp_shorts, temp_profits, temp_stop_loss
                upper_band, middle_band, lower_band = temp_upper_band, temp_middle_ban, temp_lower_band
                optimized_period, optimized_multiplier = period, multiplier

    return upper_band, middle_band, lower_band, longs, shorts,\
        profits, stop_loss, max_sharpe_ratio, optimized_period, optimized_multiplier


def annualised_sharpe(returns):
    multiplication = np.multiply(np.sqrt(returns.size), returns.mean())
    std = returns.std()

    if multiplication == 0 or std == 0:
        return 0

    return np.divide(multiplication, std)
