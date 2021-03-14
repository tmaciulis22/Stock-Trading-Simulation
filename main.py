import util
import constants

df = util.load_data(constants.MSFT_DATA_PATH)

util.plot_data(
    df[constants.DATE_COLUMN],
    df[constants.CLOSE_COLUMN],
    title=constants.MSFT_TITLE,
    toggle_grid=True,
)

upper_band, middle_band, lower_band = util.calculate_bollinger_band(df)
util.plot_data(
    df[constants.DATE_COLUMN],
    upper_band,
    color="green",
    label="Upper Bollinger Band"
)
util.plot_data(
    df[constants.DATE_COLUMN],
    lower_band,
    color="red",
    label="Lower Bollinger Band"
)
util.plot_data(
    df[constants.DATE_COLUMN],
    middle_band,
    color="black",
    label="Middle Bollinger Band"
)
util.add_bollinger_shade(df[constants.DATE_COLUMN], upper_band, lower_band)

buys, sells, profits = util.simulate_strategy(df, upper_band, lower_band)

util.scatter_data(
    df[constants.DATE_COLUMN][buys],
    df[constants.CLOSE_COLUMN][buys],
    color="red",
    label="Buys",
    marker="v"
)
util.scatter_data(
    df[constants.DATE_COLUMN][sells],
    df[constants.CLOSE_COLUMN][sells],
    color="green",
    label="Sells",
    marker="^"
)

util.toggle_legend()

util.plot_data(
    df[constants.DATE_COLUMN],
    profits.cumsum(),
    title="Profits (USD)",
    new_figure=True
)

