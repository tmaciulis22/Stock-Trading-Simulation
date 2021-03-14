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


def create_subplots():
    return plt.subplots(nrows=2, constrained_layout=True)


def plot_data(
    axis,
    x_values,
    y_values,
    title=None,
    x_label=None,
    y_label=None,
    toggle_grid=True,
    color=None,
    label=None
):
    axis.set_title(title)
    if toggle_grid:
        axis.grid()
    if x_label is not None:
        axis.set_xlabel(x_label)
    if y_label is not None:
        axis.set_ylabel(y_label)
    axis.plot(x_values, y_values, color=color, label=label)


def calculate_bollinger_band(df):
    moving_avg = np.round(df[constants.CLOSE_COLUMN].rolling(window=constants.BOLLINGER_PERIOD).mean(), 2)

    std = np.round(df[constants.CLOSE_COLUMN].rolling(window=constants.BOLLINGER_PERIOD).std(), 2)
    multiplied_std = np.multiply(std, constants.BOLLINGER_MULTIPLIER)

    upper_band = np.round(np.add(moving_avg, multiplied_std), 2)
    lower_band = np.round(np.subtract(moving_avg, multiplied_std), 2)

    return upper_band, moving_avg, lower_band
