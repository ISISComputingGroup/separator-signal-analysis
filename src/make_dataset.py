import os
import shutil

if __name__ == "__main__":
    project_root = os.path.abspath(os.getcwd())
    data_source_directory = os.path.join(r"\\ISIS", "Shares", "ISIS_Experimental_Controls", "muon_fe_separator_data")
    data_directory = os.path.join(project_root, "data")
    raw_data_directory = os.path.join(data_directory, "raw")

    # Create data directory structure
    if not os.path.exists(data_directory):
        os.mkdir(data_directory)
        print("Created data directory")

    if not os.path.exists(raw_data_directory):
        os.mkdir(raw_data_directory)
        print("Created raw data directory")

    if not os.path.exists(os.path.join(data_directory, "processed")):
        os.mkdir(os.path.join(data_directory, "processed"))
        print("Created processed data directory")

    # Copy data files
    for file_name in os.listdir(data_source_directory):
        shutil.copy(os.path.join(data_source_directory, file_name), raw_data_directory)
        print("Copied {} from {} to {}".format(file_name, data_source_directory, raw_data_directory))
