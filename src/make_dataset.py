import os
import pandas as pd

from data_processing import clean_camonitored_data


if __name__ == "__main__":

    raw_data_path = os.path.abspath(os.path.join("data", "raw"))
    processed_data_path = os.path.abspath(os.path.join("data", "processed"))

    files = os.listdir(raw_data_path)

    for filename in files:

        if filename.split(".")[-1] == "txt":
            print("Reading {} from {}".format(filename, os.path.join(raw_data_path, filename)))

            data = pd.read_csv(os.path.join(raw_data_path, filename), delim_whitespace=True, header=None)
            data = clean_camonitored_data(data)

            csv_name = "{}-cleaned.csv".format(filename.split(".")[0])
            print("Writing {} to {}".format(filename, os.path.join(processed_data_path, csv_name)))
            data.to_csv(os.path.join(processed_data_path, csv_name), index=False)
        else:
            print("Not reading data from {}.".format(filename))
