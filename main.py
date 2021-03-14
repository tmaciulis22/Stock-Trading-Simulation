import util
import constants

figure, axes = util.create_subplots()
figure.suptitle(constants.AAPL_FIGURE_TITLE, fontsize=18)

df = util.load_data(constants.APPL_DATA_PATH)

util.plot_data(
    axes[0],
    df[constants.DATETIME_COLUMN],
    df[constants.CLOSE_COLUMN],
    title="Price (USD)",
)

upper_band, middle_band, lower_band = util.calculate_bollinger_band(df)
util.plot_data(
    axes[0],
    df[constants.DATETIME_COLUMN],
    upper_band,
    toggle_grid=False,
    color="green",
    label="Upper Bollinger Band"
)
util.plot_data(
    axes[0],
    df[constants.DATETIME_COLUMN],
    lower_band,
    toggle_grid=False,
    color="red",
    label="Lower Bollinger Band"
)
util.plot_data(
    axes[0],
    df[constants.DATETIME_COLUMN],
    middle_band,
    toggle_grid=False,
    color="black",
    label="Middle Bollinger Band"
)
axes[0].fill_between(df[constants.DATETIME_COLUMN], upper_band, lower_band, color="paleturquoise")
axes[0].legend(loc="upper right")

