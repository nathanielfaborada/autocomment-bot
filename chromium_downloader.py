import os
import requests
import zipfile
import tarfile
import platform

def download_chromium():
    # Define download URLs and file names based on platform
    urls = {
        'Windows': 'https://download-chromium.appspot.com/dl/Win_x64',
        'Darwin': 'https://download-chromium.appspot.com/dl/Mac',
        'Linux': 'https://download-chromium.appspot.com/dl/Linux_x64'
    }

    file_names = {
        'Windows': 'chromium-win.zip',
        'Darwin': 'chromium-mac.zip',
        'Linux': 'chromium-linux.tar.gz'
    }

    extract_methods = {
        'Windows': lambda file: zipfile.ZipFile(file, 'r').extractall(),
        'Darwin': lambda file: zipfile.ZipFile(file, 'r').extractall(),
        'Linux': lambda file: tarfile.open(file, 'r:gz').extractall()
    }

    system = platform.system()
    if system not in urls:
        raise Exception(f"Unsupported OS: {system}")

    url = urls[system]
    file_name = file_names[system]

    # Download Chromium
    print(f"Downloading Chromium for {system}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(file_name, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    print(f"Downloaded Chromium to {file_name}")

    # Extract the downloaded file
    print(f"Extracting {file_name}...")
    extract_methods[system](file_name)

    print("Extraction complete.")

if __name__ == '__main__':
    download_chromium()