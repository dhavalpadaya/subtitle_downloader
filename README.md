# subtitle_downloader
Python script to automatically download subtitles for any movie/tv series episode from www.opensubtitles.com.

Get the latest version of Python at http://www.python.org/getit/.

Getting Started
---------------

The easiest way to get started is to clone the repository:

```bash
# Get the latest snapshot
git clone https://github.com/dhavalpadaya/subtitle_downloader.git subtitle_downloader

# Change directory
cd subtitle_downloader

# Install Guessit
# guessIt is a python library that extracts as much information as possible from a video filename. http://guessit.io
pip install guessit

# Install IMDbPY
# IMDbPY is a Python package useful to retrieve and manage the data of the IMDb movie database about movies, people, characters and companies.
pip install IMDbPY

# Then simply run python script
python subtitle_downloader.py
```

On running script, There will be two options to select from.
1. Select A Single File
  * Select a video file from file browse dialog
  * Subtitle files(1 or more than one files based on  given configuration) for that video will be downloaded and will be saved in a same folder where file is stored.
  * Text file will be generated which will have details of that movie/tv series episode from IMDB database

2. Select A Folder
  * Select a folder from file browse dialog
  * Subtitle files(1 or more than one files based on given configuration) for each movie/tv series episode in that folder will be downloaded and will be saved in a same folder where file is stored.
  * Text files will be generated for all movie/tv series episodes which will have details of that movie/tv series episode from IMDB database

**Note:** - If you have a python IDLE then simply double click on subtitle_downloader.py to run script.

Screenshots
---------------

<img src="/screenshots/001.png" alt="Subtitle Downloader"/>

<img src="/screenshots/002.png" alt="Subtitle Downloader"/>

<img src="/screenshots/003.png" alt="Subtitle Downloader"/>

<img src="/screenshots/004.png" alt="Subtitle Downloader"/>

Configuration
---------------

Set different configurations such as allowed video file extensions, subtitle language and maxsubtitles to download in config.py

```
# Write all the supported video file extensions in a tuple
videoFilesExtensionList = (".mp4", ".mkv", ".avi", ".webm", ".flv", ".3gp")
# Write Comma seperated list of all languageids or write all to search in all languages
# Run this program with command_line argument 'lang_list' to list all supported languages(Ex. python subtitle_downloader.py lang_list)
subtitleLanguages = 'eng'
# Maximum no of subtitles generated per file
maxSubtitles = 1
```

## Additional Feature

One text file of IMDB details for that movie/tv series episode will be generated along with subtitle file.

Text file will contain following details.

* Title
* Type (movie/tv series)
* Year
* Number of seasons (for tv series episodes)
* series years (for tv series episodes)
* Rating
* Votes
* Genres
* Plot Outline
* Cast
* Directors


## Development

We would love if you can contribute to make this project better. Here's how you can do it:

1. Fork the project.
2. Commit changes or bugfixes to your repo.
3. Submit a pull request
4. Sit back and relax while our maintainers checkout your changes and approve them!




