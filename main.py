import constants
import util
import calculations

df = util.load_data(constants.MSFT_DATA_PATH)

util.plot_data(
    df[constants.DATE_COLUMN],
    df[constants.CLOSE_COLUMN],
    title=constants.MSFT_TITLE,
    toggle_grid=True,
)

upper_band, middle_band, lower_band = calculations.calculate_bollinger_band(df)
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

longs, shorts, profits, stop_loss = calculations.simulate_strategy(df, upper_band, lower_band)
util.scatter_data(
    df[constants.DATE_COLUMN][longs],
    df[constants.CLOSE_COLUMN][longs],
    color="green",
    label="Longs(Buys)",
    marker="^"
)
util.scatter_data(
    df[constants.DATE_COLUMN][shorts],
    df[constants.CLOSE_COLUMN][shorts],
    color="red",
    label="Shorts(Sells)",
    marker="v"
)
util.scatter_data(
    df[constants.DATE_COLUMN][stop_loss],
    df[constants.CLOSE_COLUMN][stop_loss],
    color="black",
    label="Stop Loss",
    marker="x"
)
util.toggle_legend()

util.plot_data(
    df[constants.DATE_COLUMN],
    profits.cumsum(),
    title="Profits (USD)",
    new_figure=True,
    toggle_grid=True
)
