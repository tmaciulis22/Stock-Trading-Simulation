import pandas as pd
import matplotlib.pyplot as plt
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


def toggle_legend(): plt.legend(loc="upper left")
