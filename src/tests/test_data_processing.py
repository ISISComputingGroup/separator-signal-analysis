import datetime
import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal
from src.data_processing import create_data_from_entry, clean_camonitored_data, average_data, create_rolling_averages

from src.data_processing import flatten_data, unstable_seconds

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


class AveragingAllDataTests(unittest.TestCase):

    def test_that_GIVEN_a_row_THEN_an_array_of_rolling_averages_is_produced(self):
        # Given:
        timestamp = datetime.datetime.utcnow()
        data = pd.DataFrame(
            data=[[timestamp, i] for i in range(1, 11)],
            columns=["Datetime", "Value"]
        )

        # When:
        result = average_data(data, increment=2)

        # Then:
        expected = pd.DataFrame(
            data=[[timestamp, float(i)] for i in range(2, 10)],
            columns=["Datetime", "Value"]
        )
        assert_frame_equal(result, expected)


class CleaningCamonitoredData(unittest.TestCase):

    def test_that_GIVEN_data_obtained_by_monitoring_a_pv_THEN_the_cleaned_data_has_101_columns(self):
        # Given:
        data = pd.DataFrame(data=TEST_CAMONITORED_DATA)

        # When:
        cleaned_data = clean_camonitored_data(data)

        # Then
        self.assertEquals(len(cleaned_data.columns), 101)


class FlatteningData(unittest.TestCase):

    def test_that_GIVEN_a_row_of_values_THEN_the_values_are_flattened(self):
        # Given:
        timestamp = datetime.datetime.utcnow()

        data1 = [timestamp]
        data1.extend([i for i in range(1, 100 + 1)])
        columns = ["Datetime"]
        columns.extend(list(range(1, 100 + 1)))

        data2 = data1[:]
        data2[0] = timestamp + datetime.timedelta(seconds=1)

        data = pd.DataFrame(data=[data1, data2], columns=columns)

        # When:
        result = flatten_data(data)

        # Then:
        expected = pd.DataFrame(
            data=[[timestamp + i * datetime.timedelta(milliseconds=10), value] for i, value in enumerate(data1[1:])],
            columns=["Datetime", "Value"]
        )
        assert_frame_equal(result, expected)


class UnstableSeconds(unittest.TestCase):

    def test_that_GIVEN_100_unstable_values_THEN_all_1_second_is_unstable(self):
        # Given:
        timestamp = datetime.datetime.utcnow()

        data = pd.DataFrame(
            data=[[timestamp + i * datetime.timedelta(milliseconds=10), i] for i in range(1, 100+1)],
            columns=["Datetime", "Value"]
        )

        # When:
        result = unstable_seconds(data, -1)

        # Then:
        expected = 1.0
        self.assertEquals(result, expected)

    def test_that_GIVEN_5_stable_values_THEN_all_0_95_seconds_is_unstable(self):
        # Given:
        timestamp = datetime.datetime.utcnow()

        data = pd.DataFrame(
            data=[[timestamp + i * datetime.timedelta(milliseconds=10), i] for i in range(1, 100+1)],
            columns=["Datetime", "Value"]
        )

        # When:
        result = unstable_seconds(data, 50.0, 2, 2)

        # Then:
        expected = 0.95
        self.assertEquals(result, expected)

    def test_that_GIVEN_100_stable_values_THEN_all_0_second_are_unstable(self):
        # Given:
        timestamp = datetime.datetime.utcnow()

        data = pd.DataFrame(
            data=[[timestamp + i * datetime.timedelta(milliseconds=10), i] for i in range(1, 100 + 1)],
            columns=["Datetime", "Value"]
        )

        # When:
        result = unstable_seconds(data, 50.0, 50, 50)

        # Then:
        expected = 0
        self.assertEquals(result, expected)


class AveragingPacketOfDataTests(unittest.TestCase):

    def test_that_GIVEN_a_row_THEN_an_array_of_rolling_averages_is_produced(self):
        # Given:
        timestamp = datetime.datetime.utcnow()
        row = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, timestamp],
                        index=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "Datetime"])

        # Then:
        result = create_rolling_averages(row, increment=2)
        expected = [timestamp, 2, 3, 4, 5, 6, 7, 8, 9]

        self.assertEquals(result, expected)