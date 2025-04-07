import os
import zipfile
import requests


def check_and_prepare_data_directory(data_dir, file_url):
    # Check if the data directory exists
    if not os.path.exists(data_dir):
        raise FileNotFoundError("Data directory doesn't exist, it should at least exist and be empty, please create it")

    # Check if the directory contains any files (except the README and gitignore files)
    print(len(os.listdir(data_dir)))
    if len(os.listdir(data_dir)) < 2:
        print(f"Data directory '{data_dir}' is empty. Downloading data from {file_url}...")

        # Download the zip file
        zip_file_path = os.path.join(data_dir, "file.zip")
        response = requests.get(file_url, stream=True)

        if response.status_code == 200:
            with open(zip_file_path, 'wb') as zip_file:
                for chunk in response.iter_content(chunk_size=128):
                    zip_file.write(chunk)
            print(f"Downloaded {zip_file_path}")

            # Extract the zip file into the data directory
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(data_dir)
            print(f"Extracted data to {data_dir}")

            # Delete the zip file after extraction
            os.remove(zip_file_path)
            print(f"Deleted the zip file: {zip_file_path}")
        else:
            raise Exception(f"Failed to download the file from {file_url}, status code: {response.status_code}")
    else:
        print(f"Data directory '{data_dir}' already contains files.")

# Example usage:
# check_and_prepare_data_directory('../../Data', 'http://www.my.data/file.zip')