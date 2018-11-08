import os
import pandas as pd
from data_processing import clean_data


if __name__ == "__main__":

    raw_data_path = os.path.abspath("data\\raw")
    processed_data_path = os.path.abspath("data\\processed")

    if os.path.exists(os.path.join(processed_data_path, "cleaned_data.csv")):
        print("Deleting an old copy")
        os.remove(os.path.join(processed_data_path, "cleaned_data.csv"))

    print("Reading data from {}".format(raw_data_path))
    data = pd.read_csv(os.path.join(raw_data_path, "muon_results.csv"), header=None)

    data = clean_data(data)

    print("Writing data to {}".format(processed_data_path))
    data.to_csv(os.path.join(processed_data_path, "cleaned_data.csv"), index=False)
