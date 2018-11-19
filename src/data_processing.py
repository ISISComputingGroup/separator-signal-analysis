from __future__ import division
import pandas as pd
import numpy as np


def create_data_from_entry(row_number, raw_dataframe):
    """
    Creates a dataframe with timestamps from a row of data.

    Args:
        row_number (int): Row number to turn into a dataframe
        raw_dataframe (pandas dataframe): The raw dataframe whose rows are to be be converted.

    Returns:
        dataframe: A pandas dataframe whose index is a list of timestamps and whose entries are the values
            of a row.
    """
    raw_dataframe["Datetime"] = pd.to_datetime(raw_dataframe["Datetime"])

    row = raw_dataframe.iloc[row_number]

    base_timestamp = row.loc["Datetime"].to_datetime64()
    time_delta = (raw_dataframe.loc[row_number + 1, "Datetime"].to_datetime64()
                  - base_timestamp) / 100
    new_time_stamps = [np.datetime64(base_timestamp + i * time_delta) for i in range(0, row.size + 1)]

    row = row.drop("Datetime")
    dataframe = pd.DataFrame(data=zip(new_time_stamps, row.values), columns=["Datetime", "Value"])
    dataframe = dataframe.sort_index(axis=1)
    return dataframe


def calibrate_data(dataframe, calibration_factor):
    """
    Calibrates a dataframe by a calibration_factor.

    Calibrates a dataframe with data columns 1-100 and a Datetime column.

    Args:
        dataframe (pandas dataframe): Pandas dataframe to calibrate.
        calibration_factor (float): The calibration factor.

    Returns:
        pandas dataframe: Calibrated dataframe.
    """

    calibrated_data = dataframe.loc[:, list(range(1, 100 + 1))]
    calibrated_data = calibrated_data.applymap(lambda x: x * calibration_factor)
    calibrated_data["Datetime"] = pd.to_datetime(dataframe["Datetime"])
    calibrated_data = calibrated_data.drop_duplicates()
    calibrated_data = calibrated_data.reset_index(drop=True)
    return calibrated_data


def clean_camonitored_data(data):
    """
    Cleans file produced from camonitoring a PV.

    Args:
        data (pandas Dataframe): Pandas Dataframe to be parsed.
    Returns:
        cleaned_dataframe (Dataframe): Cleaned dataframe
    """
    columns = ["PV name", "Date", "Time", "NELM"]
    columns.extend(list(range(1, 100 + 1)))
    data.columns = columns

    data["Datetime"] = pd.to_datetime(data["Date"] + ' ' + data["Time"])

    new_columns = ["Datetime"]
    new_columns.extend(list(range(1, 100 + 1)))
    cleaned_dataframe = data[new_columns]

    return cleaned_dataframe


def unstable_seconds(dataframe, mean, high_limit=1.0, low_limit=1.0, sampling_rate=100):
    """
    Finds the number of seconds values are outside a stability range.

    Args:
        dataframe: Dateframe to search for unstable values. Expected to have a "Value" column
        mean (float): Mean value.
        high_limit (float, optional): High limit of stability.
        low_limit (float, optional): Low limit of stability.
        sampling_rate (float, optional): The number of samples sampled per second.

    Returns:
        float: Number of unstable seconds.
    """
    unstable_readings = dataframe[(dataframe["Value"] > mean + high_limit) |
                                  (dataframe["Value"] < mean - low_limit)]
    return float(unstable_readings["Value"].size / sampling_rate)


def flatten_data(dataframe):
    """
    Flattens a dataframe and creates timestamps at equal distances from each other

    Args:
        dataframe: The data frame with rows containing packets of data with a timestamp.

    Returns:
        dataframe: A new dataframe with two columns, "Datetime" and "Value" which
    """

    flatten_seconds = pd.concat([create_data_from_entry(i, dataframe) for i in range(0, dataframe.shape[0] - 1)])
    flatten_seconds = flatten_seconds.reset_index(drop=True)
    return flatten_seconds


def average_data(dataframe, increment=1):
    """
    Average pairs of elements in a dataframe.

    Expected schema for the dataframe is:
        - Datetime: Date and time associated to a value.
        - Value: A value.

    Args:
        dataframe: Pandas Dataframe to average
        increment: Increment between entries to avearge.

    Returns:
        Dataframe of averaged values.
    """
    def average_pairs(index):
        return np.mean([dataframe.loc[index, "Value"], dataframe.loc[index + increment, "Value"]])

    number_of_rows = len(dataframe.index)
    averaged_data = pd.DataFrame(
        data=[
            [dataframe.loc[i, "Datetime"], average_pairs(i)]
            for i in range(0, number_of_rows - increment)
        ],
        columns=["Datetime", "Value"]
    )
    return averaged_data
