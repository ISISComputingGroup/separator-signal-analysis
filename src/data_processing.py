import pandas as pd


def clean_data(dataframe):
    """
    Sets the columns of the dataframe and removes duplicates

    Args:
        dataframe: Pandas data frame with columns labeled 0-101.
            First column is time and next 100 are voltage readings.

    Returns:
        dataframe: Dataframe with converted columns and duplicates removed.
    """

    dataframe["Time"] = pd.to_datetime(dataframe[0], unit="s")
    dataframe = dataframe.drop(0, 1)
    dataframe = dataframe.set_index("Time")
    dataframe = dataframe.drop_duplicates(list(range(1, 100 + 1)))
    return dataframe



