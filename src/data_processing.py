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
    dataframe["Datetime"] = pd.to_datetime(dataframe[0], unit="s")
    dataframe = dataframe.drop(0, 1)
    dataframe = dataframe.drop_duplicates(list(range(1, 100 + 1)))
    dataframe = dataframe.reset_index(drop=True)
    return dataframe


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

    row = raw_dataframe.iloc[row_number]
    base_timestamp = row.loc["Datetime"].to_datetime64()
    time_delta = (raw_dataframe.loc[row_number + 1, "Datetime"].to_datetime64()
                  - base_timestamp) / 100

    new_time_stamps = [np.datetime64(base_timestamp + i * time_delta) for i in range(0, row.size + 1)]

    row = row.drop("Datetime")
    dataframe = pd.DataFrame(data=zip(new_time_stamps, row.values))
    dataframe.columns = ["Datetime", "Value"]
    dataframe = dataframe.sort_index(axis=1)
    return dataframe


def create_rolling_averages(row, increment=10):
    """
    Creates an array of rolling averages
    :param row:
    Return:
        averages (list): Row for a pandas dataframe with rolling averages.
    """

    averages = []
    averages.append(row["Datetime"])
    row = row.drop("Datetime")
    for i in range(1, row.size - increment):
        averages.append(np.mean([row[i], row[i + increment]]))

    return averages


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


def unstable_seconds(dataframe, mean, high_limit=1.0, low_limit=1.0):
    """
    Finds the number of seconds values are outside a stability range.

    Args:
        dataframe:
        mean (float): Mean value.
        high_limit (float): High limit of stability.
        low_limit (float): Low limit of stability.

    Returns:
        float: Number of unstable seconds.
    """
    try:
        unstable_readings = dataframe[(dataframe["Value"] > mean + high_limit) |
                                      (dataframe["Value"] < mean - low_limit)]
    except AttributeError:
        raise ValueError("Mean")
    return unstable_readings["Value"].size/100.0


def calibrate_data(dataframe, calibration_factor):
    """
    Calibrates a dataframe by a calibration_factor.

    Calibrates a dataframe with data columns 1-100 and a Datetime column.

    Args:
        dataframe (pandas dataframe): Pandas dataframe to calibrate.
        calibration_factor (int):

    Returns:
        pandas dataframe: Calibrated dataframe.
    """
    calibrated_data = dataframe.iloc[:, 1:100 + 1].applymap(lambda x: x * calibration_factor)
    calibrated_data["Datetime"] = pd.to_datetime(dataframe["Datetime"])
    calibrated_data = calibrated_data.drop_duplicates()
    calibrated_data = calibrated_data.reset_index(drop=True)
    return calibrated_data


def flatten_data(dataframe):
    """
    Flattens a dataframe.

    Args:
        dataframe:
    Returns:
        dataframe:
    """
    flatten_seconds = pd.concat([create_data_from_entry(i, dataframe) for i in range(0, dataframe.shape[0] - 1)])
    flatten_seconds = flatten_seconds.reset_index(drop=True)
    return flatten_seconds


def average_data(dataframe):
    """
    Average pairs of elements in a dataframe.

    Expected schema for the dataframe is:
        - Datetime: Date and time assoicated to value
        - Value

    Args:
        dataframe:

    Returns:

    """
    def average_pairs(index):
        return np.mean([dataframe.loc[index, "Value"], dataframe.loc[index + 1, "Value"]])

    number_of_rows = len(dataframe.index)
    averaged_data = pd.DataFrame(
        data=[
            [dataframe.loc[i, "Datetime"], average_pairs(i)]
            for i in range(0, number_of_rows - 1)
        ],
        columns=["Datetime", "Value"]
    )
    return averaged_data
