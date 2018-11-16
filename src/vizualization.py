import altair as alt
import numpy as np
import pandas as pd

LINE_COLOUR = "#838DB7"


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

    opacity_level = 0.8
    mean_rule_color = "#469E74"
    limits_rule_color = "#D6726B"

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
