import datetime
import unittest

import pandas as pd
from src.data_processing import create_data_from_entry, create_rolling_averages, clean_camonitored_data
from test_data import SMALL_TEST_DATA, TEST_CAMONITORED_DATA, TEST_ROWS_OF_DATA


class CreateDataFromEntryTests(unittest.TestCase):

    @staticmethod
    def _clean_data(dataframe):
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

    def test_that_GIVEN_cleaned_data_WHEN_create_data_from_array_is_called_THEN_the_first_entry_has_the_same_time_stamp(
            self):
        # Given:
        data = pd.DataFrame(
            data=SMALL_TEST_DATA, columns=list(range(0, 100 + 1))
        )
        data = self._clean_data(data)

        # When:
        result = create_data_from_entry(0, data)

        # Then:
        expected_timestamp = data.loc[0, "Datetime"]
        result_timestamp = result.loc[0, "Datetime"]
        self.assertEquals(result_timestamp, expected_timestamp)

    def test_that_GIVEN_cleaned_data_WHEN_create_data_from_array_is_called_THEN_the_first_entry_has_the_same_value(
            self):
        # Given:
        data = pd.DataFrame(
            data=SMALL_TEST_DATA, columns=list(range(0, 100 + 1))
        )
        data = self._clean_data(data)

        # When:
        result = create_data_from_entry(0, data)

        # Then:
        expected_value = 4.5185524610000005
        result_value = result.iloc[0, 1]
        self.assertEquals(expected_value, result_value)

    def test_that_GIVEN_row_with_timestamp_WHEN_create_data_from_array_is_called_THEN_the_first_entry_is_correct(
            self):
        # Given:
        columns = ["Datetime"]
        columns.extend(list(range(1, 91)))

        data = pd.DataFrame(
            data=TEST_ROWS_OF_DATA,
            columns=columns
        )

        # When:
        result = create_data_from_entry(0, data)

        # Then:
        expected_value = 4.4968738570000006
        result_value = result.iloc[0, 1]
        self.assertEquals(expected_value, result_value)

    def test_that_GIVEN_cleaned_data_WHEN_create_data_from_array_is_called_THEN_the_first_entry_is_not_a_time(
            self):
        # Given:
        data = pd.DataFrame(
            data=SMALL_TEST_DATA, columns=list(range(0, 100 + 1))
        )
        data = self._clean_data(data)
        data.drop(0, inplace=True)

        # When:
        result = create_data_from_entry(0, data)

        # Then:
        expected_value = 4.662332613999999
        result_value = result.iloc[0, 1]
        self.assertEquals(expected_value, result_value)


class RollingAveragesTests(unittest.TestCase):

    def test_that_GIVEN_a_row_THEN_an_array_of_rolling_averages_is_produced(self):
        # Given:
        timestamp = datetime.datetime.utcnow()
        row = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, timestamp],
                        index=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "Datetime"])

        # Then:
        result = create_rolling_averages(row, increment=2)
        expected = [timestamp, 2, 3, 4, 5, 6, 7, 8, 9]

        self.assertEquals(result, expected)


class CleaningCamonitoredData(unittest.TestCase):

    def test_that_GIVEN_data_obtained_by_monitoring_a_pv_THEN_the_cleaned_data_has_101_columns(self):
        # Given:
        data = pd.DataFrame(data=TEST_CAMONITORED_DATA)

        # When:
        cleaned_data = clean_camonitored_data(data)

        # Then
        self.assertEquals(len(cleaned_data.columns), 101)
