import pandas as pd
import numpy as np


def clean_data(dataframe):
    """
    Sets the columns of the dataframe and removes duplicates

    Args:
        dataframe: Pandas data frame with columns labeled 0-101.
            First column is time and next 100 are voltage readings.

    Returns:
        dataframe: Dataframe with converted columns and duplicates removed.
    """
    dataframe = convert_time(dataframe)
    dataframe = dataframe.drop_duplicates(list(range(1, 100 + 1)))
    return dataframe


def create_data_from_entry(row_number, raw_dataframe):
    """
    Creates a dataframe with timestamps from a row of data.

    Args:
        row_number (int): Row number to turn into a datafrane
        raw_dataframe (pandas dataframe): The raw dataframe whose rows are to be be converted.

    Returns:
        dataframe: A pandas dataframe whose index is a list of timestamps and whose entries are the values
            of a row.
    """

    row = raw_dataframe.iloc[row_number]
    time_delta = np.timedelta64(1, 'ms')

    new_time_stamps = []
    previous_timestamp = row.loc["Time"].to_datetime64()
    row = row.drop("Time")

    for i in range(row.size):
        if i == 0:
            new_time_stamps.append(previous_timestamp)
        else:
            new_time_stamp = previous_timestamp + time_delta
            new_time_stamps.append(new_time_stamp)
            previous_timestamp = new_time_stamp

    dataframe = pd.DataFrame(data=zip(new_time_stamps, row.values))
    dataframe = convert_time(dataframe)
    dataframe.columns = ["Value", "Time"]
    return dataframe


def convert_time(dataframe):
    """
    Converts the 0 column to a time and sets the index to time.

    Args:
        dataframe (pandas dataframe): The dataframe to covnert the index to time

    Returns:
        dataframe: The converted dataframe
    """

    dataframe["Time"] = pd.to_datetime(dataframe[0], unit="s")
    dataframe = dataframe.drop(0, 1)
    return dataframe


def load_data(nrows=None):
    """
    Loads the data and turns the time into timestamps.

    Args:
        nrows (int, optional): Number of rows to import.

    Returns:
        data: A pandas dataframe of the import data.
    """
    if nrows is not None:
        data = pd.read_csv("data\\processed\\cleaned_data.csv", nrows=nrows)
    else:
        data = pd.read_csv("data\\processed\\cleaned_data.csv")

    data["Time"] = pd.to_datetime(data["Time"])

    return data


def create_rolling_averages(row, increment=10):
    """
    Creates an array of rolling averages
    :param row:
    Return:
        dataframe: Pandas dataframe of rolling averages and time stamp for each
    """

    averages = []
    averages.append(row["Time"])
    row = row.drop("Time")
    for i in range(0, row.size - increment):
        averages.append(np.mean([row[i], row[i + increment]]))

    return averages
