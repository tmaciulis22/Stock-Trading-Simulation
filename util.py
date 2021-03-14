import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import constants


def load_data(path):
    df = pd.read_csv(path)
    df[constants.DATETIME_COLUMN] = df[constants.DATE_COLUMN] + " " + df[constants.TIME_COLUMN]
    df[constants.DATETIME_COLUMN] = pd.to_datetime(df[constants.DATETIME_COLUMN], format=constants.DATETIME_FORMAT)
    df[constants.TIME_COLUMN] = pd.to_datetime(df[constants.TIME_COLUMN], format=constants.TIME_FORMAT)
    df[constants.DATE_COLUMN] = pd.to_datetime(df[constants.DATE_COLUMN], format=constants.DATE_FORMAT)

    return df


def plot_data(
    x_values,
    y_values,
    new_figure=False,
    title=None,
    toggle_grid=False,
    color=None,
    label=None
):
    if new_figure:
        plt.figure()
    if title is not None:
        plt.title(title)
    if toggle_grid:
        plt.grid()
    plt.plot(x_values, y_values, color=color, label=label)


def scatter_data(
    x_values,
    y_values,
    color=None,
    marker=None,
    label=None
): plt.scatter(x_values, y_values, c=color, label=label, marker=marker, s=9**2)


def add_bollinger_shade(
    dates,
    upper_band,
    lower_band
):
    plt.fill_between(dates, upper_band, lower_band, color="paleturquoise")


def toggle_legend(): plt.legend(loc="upper right")


def calculate_bollinger_band(df):
    moving_avg = np.round(df[constants.CLOSE_COLUMN].rolling(window=constants.BOLLINGER_PERIOD).mean(), 2)

    std = np.round(df[constants.CLOSE_COLUMN].rolling(window=constants.BOLLINGER_PERIOD).std(), 2)
    multiplied_std = np.multiply(std, constants.BOLLINGER_MULTIPLIER)

    upper_band = np.round(np.add(moving_avg, multiplied_std), 2)
    lower_band = np.round(np.subtract(moving_avg, multiplied_std), 2)

    return upper_band, moving_avg, lower_band


# def simulate_strategy(df, upper_band, lower_band):
#     should_sell = False
#     prices = df[constants.CLOSE_COLUMN]
#     buys = np.full(prices.shape, False)
#     sells = np.full(prices.shape, False)
#     profits = np.zeros_like(prices)
#     buying_price = 0
#
#     for i in range(constants.BOLLINGER_PERIOD, len(df.index)):
#         if prices[i] <= lower_band[i] and not should_sell:
#             should_sell = True
#             buys[i] = True
#             total_price = prices[i] * constants.NO_OF_SHARES
#             buying_price = total_price - total_price * constants.TRADING_FEE
#         if prices[i] >= upper_band[i] and should_sell:
#             should_sell = False
#             sells[i] = True
#             total_price = prices[i] * constants.NO_OF_SHARES
#             profits[i] = (total_price - total_price * constants.TRADING_FEE) - buying_price
#
    # return buys, sells, profits

def simulate_strategy(df, upper_band, lower_band):
    should_sell = False
    prices = df[constants.CLOSE_COLUMN]
    buys = np.full(prices.shape, False)
    sells = np.full(prices.shape, False)
    profits = np.zeros_like(prices)

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
        if prices[i] >= upper_band[i] and should_sell:
            should_sell = False
            sells[i] = True

    return buys, sells, profits
