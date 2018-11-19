import os
import shutil

if __name__ == "__main__":
    project_root = os.getcwd()
    data_source_directory = os.path.join(r"\\ISIS", "Shares", "ISIS_Experimental_Controls", "muon_fe_separator_data")
    print(data_source_directory)
    data_destination_directory = os.path.join(project_root, "data", "raw")
    print(data_destination_directory)

    for file_name in os.listdir(data_source_directory):
        shutil.copy(os.path.join(data_source_directory, file_name), data_destination_directory)
        print("Copied {} from {} to {}".format(file_name, data_source_directory, data_destination_directory))
