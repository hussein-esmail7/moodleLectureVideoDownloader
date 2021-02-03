# moodleLectureVideoDownloader
## Description
This video downloads all the videos from Moodle online lectures into one folder.

This program is made for macOS. It first opens the "Backup and Sync from Google" application (the Desktop Google Drive application for macOS), then uses a chromedriver with the selenium library to download the videos.

Make sure when running, to put in your own file paths and moodle login for https://moodle.info.yorku.ca

## Installation
Copy and paste this command to download this repository after you've changed directories to the folder you want.
```
git clone https://github.com/hussein-esmail7/moodleLectureVideoDownloader
```
Then change directories into that folder.
```
cd moodleLectureVideoDownloader
```
If you have python3 installed, you can install the required libraries via pip:
```
pip install requirements.txt
```
While this is happening, you can edit variables.py to add in your path to chromedriver and username and passwords to your email and York Moodle. Email is required if you want the program to send you email notifications to yourself and other people that a specific video was added to its destination folder.

After that is done, you can now run the movieConverter program.
```
python3 mainFile.py
```
