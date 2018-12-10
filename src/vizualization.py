import altair as alt
import numpy as np
import pandas as pd

LINE_COLOUR = "#7570b3"


def generate_line_chart(x_title="", y_title="", y_scale=(83, 97), time_unit="secondsmilliseconds"):
    """
    Generates a line chart to visualize the signal.

    Args:
        x_title (string, optional): X axis title. Defaults to "".
        y_title (string, optional): Y azis title. Defaults to "".
        y_scale (tuple, optional): Scale for the Y axis. Defaults to (83, 97).
        time_unit (string, optional): Defaults to "secondsmilliseconds".

    Returns:
        base: altair line chart class to plot "Datetime:T" against "Value:Q".
    """
    base = alt.Chart().mark_line(color=LINE_COLOUR).encode(
        x=alt.X("Datetime:T",
                timeUnit=time_unit,
                title=x_title
                ),
        y=alt.Y("Value:Q",
                scale=alt.Scale(domain=list(y_scale)),
                title=y_title)
    )

    return base


def generate_stability_rules(dataframe, column="Value"):
    """
    Generates mean and upper and lower stability bounds for visualizations
    using a dataframe.

    Args:
        dataframe (dataframe): Pandas dataframe to get the mean from
        column (string, optional): Column to calculate the mean from.
            Default to "Value".
    Returns:
        altair layer chart with horizontal lines for mean, lower  stability limit and upper stability limit.
    """

    opacity_level = 1
    mean_rule_color = "#1b9e77"
    limits_rule_color = "#d95f02"

    limit_data = pd.DataFrame([{
        'average': np.mean(dataframe.loc[:, column]),
        'low_limit': np.mean(dataframe.loc[:, column]) - 1,
        'high_limit': np.mean(dataframe.loc[:, column]) + 1
    }])

    mean = alt.Chart().mark_rule(color=mean_rule_color, opacity=opacity_level).encode(
        y="average:Q",
        size=alt.value(3)
    )

    low_limit = alt.Chart().mark_rule(color=limits_rule_color, opacity=opacity_level).encode(
        y="low_limit:Q",
        size=alt.value(3)
    )

    high_limit = alt.Chart().mark_rule(color=limits_rule_color, opacity=opacity_level).encode(
        y="high_limit:Q",
        size=alt.value(3)
    )

    return alt.layer(mean, high_limit, low_limit, data=limit_data)
