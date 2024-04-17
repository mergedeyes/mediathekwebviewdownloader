# MediathekViewWeb-Downloader

## Disclaimer
This script has been coded with the help of ChatGPT 4.
This repository and its contents are not officially associated with, endorsed by, or sponsored by the original creators or maintainers of `mediathekviewweb` or any of its projects. The use of the `mediathekviewweb` name, API, or any related materials in this project is for descriptive purposes only and does not imply any official affiliation or endorsement.

This Python script facilitates searching for and downloading media content based on title and channel from `mediathekviewweb.de`. It supports different qualities for download and provides an intuitive command-line interface for interaction.

## Features

- **Compatibility**: Tested on **Windows 11 Pro 23H2 (Build 22631.3374)** and **Ubuntu 23.10 (Mantic Minotaur)** on 10th April, 2024.
- **Search by Title and Channel**: Enables users to find media content using specific titles and channels.
- **Quality Selection**: Users can select the media quality (Standard, Low, HD) before downloading.
- **Human-readable File Sizes**: Displays file sizes in an easy-to-understand format.
- **Filename Sanitization and Customization**: Automatically removes illegal characters from filenames and allows for custom filename inputs.
- **Download Progress Indicator**: Shows download progress, speed, and estimated time until completion.

## Requirements

To run this script, you need Python 3.11.6 or higher and the following packages:
- `requests`
- `prompt_toolkit`

The `re`, `json`, `time`, and `os` modules are part of the Python Standard Library and do not require separate installation.

You can install the necessary packages using pip:

```sh
python3 -m pip install requests prompt_toolkit
```

## Usage

1. **Running the Script**:
   Navigate to the script's directory in your terminal and run:

   ```sh
   python3 script_name.py
   ```

   Replace `script_name.py` with the actual name of the script.

2. **Input Search Criteria**:
   When prompted, input the title and channel for the media content you are searching for.

3. **Select an Episode**:
   Choose from the list of episodes presented based on your search criteria.

4. **Choose Quality**:
   Select the desired quality for your download.

5. **Filename Customization**:
   Input a custom filename for your download or press enter to use the default filename suggested by the script.

6. **Overwrite Confirmation**:
   If a file with the chosen filename already exists, you'll be prompted to confirm whether you wish to overwrite it.

## Handling Interruptions

To stop the script during execution, press `Ctrl+C`. The script will exit gracefully, notifying you that the operation was cancelled by the user.

## Troubleshooting

Ensure all [requirements](#requirements) are properly installed if you encounter any errors related to missing modules. Check your internet connection and the availability of `mediathekviewweb.de` if you face other issues.

## Author

- Jan Motulla - DE
- [GitHub](https://github.com/mergedeyes/)
- Contact: github@mergedcloud.de
