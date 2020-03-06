"""
Downloading Video Recordings from Moodle
Hussein Esmail
Created: January 9, 2020
Description: This video downloads all the videos from Andrew Skelton's lectures into one folder, and asks where that
    folder would be if the default folder is not present: ~/Google Drive/Shared/Skelton Video Lectures
Note: This program was made for the macOS operating system
"""

# IMPORT STATEMENTS
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys  # For pressing 'enter'
import urllib.request
from urllib.request import urlopen
import subprocess
import getpass
import time
import os
import sys
from termcolor import colored  # Does cool-looking print statements when run in the Terminal
from selenium.webdriver.chrome.options import Options
import smtplib
from email.mime.text import MIMEText

sys.path.insert(1, "/Users/hussein/PycharmProjects/reference")  # Python file where passwords are stored
import variables  # Import the variables from variables.py which is in the above file path


def main():
    # VARIABLES
    boolTestMode = False
    boolOpenGoogleDrive = True
    boolRunInBackground = True
    boolPrintNumOfVideosOnSite = False
    boolPrintVideoListToDownload = True
    boolPrintVideoExists = False
    boolPrintProgramDone = True
    boolPrintEmailSentToEachPerson = True
    boolPrintFileSizes = True
    boolPrintDoneWaiting = False

    colorAlreadyExists = 'yellow'
    colorEmailSentTo = 'cyan'
    colorIntro = 'cyan'
    colorNoMore = 'red'
    colorProgramDone = 'white'
    colorVideoDownloaded = 'green'
    colorWaitingDone = 'green'
    colorWaitingStart = 'white'

    intDelayLoginWait = 7
    intDelayShort = 2
    intDelayLong = 4
    intDelayIfError = 20  # Wait x seconds if there is an error to give it enough time to load

    strFileExtensionToSaveAs = ".mp4"
    strGoogleDriveApplicationPath = "/Applications/Backup and Sync.app"
    strYorkUsername = getpass.getuser()  # Username of the computer that this is being run on
    strChromedriverPath = variables.chromedriverPath
    strPathToSaveVideos = "/Users/" + strYorkUsername + "/Google Drive/Shared/Skelton Video Lectures/"
    strTargetSite = "https://moodle.info.yorku.ca"
    strSkeltonMoodleLink = "https://moodle.yorku.ca/moodle/course/view.php?id=154768"  # Used after moodle is signed in
    strYorkUsername = variables.loginYorkUsername
    strYorkPassword = variables.loginYorkPassword
    strGmailSenderEmail = variables.loginGoogleUsername
    strGmailSenderPassword = variables.loginGooglePassword
    strIntro = "Skelton Lecture Video Downloader\nCreated by Hussein Esmail"
    strLoadingMessage = "Loading..."
    strLoadingDoneMessage = "Done waiting."
    strNoMoreFilesToDownload = "No more videos to download."
    strInputDirectory = "Default directory does not exist. \n\tWhere do you want the videos to go?\nDIR >>> "
    strRemainingToDownload = "Getting videos from these days: "
    strStartingDownload = "Starting download..."
    strEmailSubjectSingular = "New MATH 1014 video uploaded to Google Drive"
    strEmailSubjectPlural = "New MATH 1014 video(s) uploaded to Google Drive"
    strEmailInitialMessage = "This is an email from Hussein's MATH 1014 Lecture Recording Video Program\n" \
                             "These videos have been downloaded:\n"
    strEmailSentTo = "Notification email sent to: "
    strEmailsToNotify = []  # Array of emails to notify after a video has been downloaded
    if boolTestMode:
        strEmailsToNotify = []  # TEMPORARY, for testing mode. Your own email would go here

    xPathLoginButton = "/html/body/div[1]/div[1]/div/div/article/div/section/section/a[1]/button"
    xPathUsername = "/html/body/div[3]/div[2]/div[1]/form/div[1]/div[2]/p/input"
    xPathPassword = "/html/body/div[3]/div[2]/div[1]/form/div[2]/div[2]/p[1]/input"
    xPathLectureRecordings = "/html/body/div[2]/div[2]/div/div/section[1]/div/div/ul/li[1]/div[3]/ul/li[5]" \
                             "/div/div/div[2]/div/a"
    xPathDateButton1 = "/html/body/div[2]/div[2]/div/div/section/div[2]/div[2]/table/tbody/tr["
    xPathDateButton2 = "]/td[2]/a"
    xPathVideoLink = "/html/body/div[1]/div[2]/div/div/section/div[1]/div/article/div[1]/div/div/div[2]/div[1]/a"

    elementDateButtons = []
    elementDates = []

    print(colored(strIntro, colorIntro))
    if boolOpenGoogleDrive:  # Open Google Drive Backup application
        subprocess.call(["/usr/bin/open", "-W", "-n", "-a", strGoogleDriveApplicationPath])
    chrome_options = Options()
    if boolRunInBackground:
        chrome_options.add_argument("--headless")  # now Chrome will run in the background
    driver = webdriver.Chrome(strChromedriverPath, options=chrome_options)  # Open Chrome
    driver.get(strTargetSite)
    try:
        buttonLogin = driver.find_element_by_xpath(xPathLoginButton)  # Selecting continue button
        buttonLogin.click()  # Pressing Continue after the drop down menu, to get to the list of registered courses
    except Exception as e:
        print("Unexpected loading delay. L96" + str(e))
        time.sleep(intDelayIfError)
        buttonLogin = driver.find_element_by_xpath(xPathLoginButton)  # Selecting continue button
        buttonLogin.click()  # Pressing Continue after the drop down menu, to get to the list of registered courses
    print(colored(strLoadingMessage, colorWaitingStart))
    time.sleep(intDelayLong)

    try:
        inputUsername = driver.find_element_by_xpath(xPathUsername)  # Select the username field
        inputUsername.send_keys(strYorkUsername)  # Type in the username
    except Exception as e:
        print("Error line 77: " + str(e))
        time.sleep(intDelayIfError)
        inputUsername = driver.find_element_by_xpath(xPathUsername)  # Select the username field
        inputUsername.send_keys(strYorkUsername)  # Type in the username
    time.sleep(intDelayShort)  # Delay between typing username and password
    try:
        inputPassword = driver.find_element_by_xpath(xPathPassword)  # Select the password field
        inputPassword.send_keys(strYorkPassword + Keys.RETURN)  # Type in the password
    except Exception as e:  # If the page is not loaded yet
        print("Error line 140: " + str(e))
        time.sleep(intDelayIfError)  # Wait a few seconds then try again
        inputPassword = driver.find_element_by_xpath(xPathPassword)  # Select the password field
        inputPassword.send_keys(strYorkPassword + Keys.RETURN)  # Type in the password
    time.sleep(intDelayLoginWait)  # Wait for browser to open next page
    try:
        driver.get(strSkeltonMoodleLink)
    except NoSuchElementException:  # If the element is not there yet
        time.sleep(intDelayIfError)  # Wait a few seconds and click again
        driver.get(strSkeltonMoodleLink)
    time.sleep(intDelayLong)
    try:
        buttonLectureRecordings = driver.find_element_by_xpath(xPathLectureRecordings)
        buttonLectureRecordings.click()
    except NoSuchElementException:  # Try 2
        time.sleep(intDelayIfError)
        try:
            buttonLectureRecordings = driver.find_element_by_xpath(xPathLectureRecordings)
            buttonLectureRecordings.click()
        except NoSuchElementException:  # Try 3
            time.sleep(intDelayIfError)
            buttonLectureRecordings = driver.find_element_by_xpath(xPathLectureRecordings)
            buttonLectureRecordings.click()
    time.sleep(intDelayLong)
    if boolPrintDoneWaiting:
        print(colored(strLoadingDoneMessage, colorWaitingDone))

    # Counting the videos and saving the dates for the titles
    i = 1
    while True:
        try:
            xPathTemporary = xPathDateButton1 + str(i) + xPathDateButton2
            elementDateButtons.append(driver.find_element_by_xpath(xPathTemporary).get_attribute('href'))
            elementDates.append(driver.find_element_by_xpath(xPathTemporary).text)
            i += 1
        except NoSuchElementException:
            if boolPrintNumOfVideosOnSite:
                print(str(len(elementDateButtons)) + " videos exist on website.")
            # print(str(elementDates))
            break

    # Changing directory to where you want the videos
    try:
        os.chdir(strPathToSaveVideos)
    except FileNotFoundError:
        strPathToSaveVideos = input(strInputDirectory)
        try:
            os.chdir(strPathToSaveVideos)
        except Exception as e:
            print("Error (164): " + str(e))
            print("\nEntered text was not a directory or does not exist. Please run this program again.")
            sys.exit()

    # Getting what files are in that folder
    arrayItemsInFolderInitial = os.listdir(strPathToSaveVideos)

    for i in range(0, len(arrayItemsInFolderInitial)):
        if arrayItemsInFolderInitial[i].find(strFileExtensionToSaveAs) != -1:
            arrayItemsInFolderInitial[i] = arrayItemsInFolderInitial[i][:-len(strFileExtensionToSaveAs)]
            # Removes the .mp4 in each video file list

    intIndexesToDelete = []
    for iFolder in range(0, len(arrayItemsInFolderInitial)):
        for iPendingDownload in range(0, len(elementDates)):
            if elementDates[iPendingDownload].find(arrayItemsInFolderInitial[iFolder]) != -1:
                intIndexesToDelete.append(iPendingDownload)

    counter = 0
    intIndexesToDelete = sorted(intIndexesToDelete, reverse=True)  # Sorts numbers highest to lowest
    for i in intIndexesToDelete:  # not range(0, len(intIndexesToDelete)) b/c intIndexesToDelete is which ones to delete
        # Ex. intIndexesToDelete = [3, 6]. Only delete elements 3 and 6
        if boolPrintVideoExists:
            print(colored(elementDates[i] + " already exists", colorAlreadyExists))
        del elementDates[i]  # Remove the entries that have already been downloaded
        del elementDateButtons[i]
        counter += 1
    if elementDates:  # If elementDates is not empty (if it's not [])
        if boolPrintVideoListToDownload:
            print(strRemainingToDownload + '\n\t- '.join(elementDates))
        print(strStartingDownload)
    else:
        print(colored(strNoMoreFilesToDownload, colorNoMore))

    strEmailUpdatedMessage = strEmailInitialMessage  # This exists to compare if the final message is
    # equal to the original. If it is not equal, notify the registered people

    for j in range(0, len(elementDateButtons)):  # Download the videos that are not already in the folder
        driver.execute_script("window.open('');")  # Make a new window
        driver.switch_to.window(driver.window_handles[1])  # Switch to new window
        driver.get(elementDateButtons[j])  # Open the date video link
        time.sleep(intDelayShort)  # While page loads
        videoButton = driver.find_element_by_xpath(xPathVideoLink)  # Open the link that leads to the video
        videoButton.click()  # Open the link that leads to the video
        time.sleep(intDelayShort)  # While the page loads
        # Get the current link (because the video file is a simple alteration to url)
        current_url = driver.current_url[:-5] + "/media/video.mp4"  # Convert current url to video url
        video_name = elementDates[j] + strFileExtensionToSaveAs
        urllib.request.urlretrieve(current_url, video_name)  # This line actually downloads
        strTempGoingToPrintAnyway = colored("\tVideo downloaded: ", colorVideoDownloaded) + video_name
        if boolPrintFileSizes:
            # These next 2 lines are gor getting the file size of each downloaded video
            site = urlopen(current_url)
            intFileSize = int(site.length)
            strFileSizeInMb = " (" + str(intFileSize*0.000001) + " MB)"
            strTempGoingToPrintAnyway = strTempGoingToPrintAnyway + strFileSizeInMb
        print(strTempGoingToPrintAnyway)  # Notifying user that a video downloaded
        strEmailUpdatedMessage = strEmailUpdatedMessage + "\t- " + video_name + "\n"
        driver.close()  # Close the current window
        driver.switch_to.window(driver.window_handles[0])  # Switch back to main window
    driver.close()  # Close the main window when the program is finished using Chrome
    if strEmailUpdatedMessage != strEmailInitialMessage:
        s = smtplib.SMTP('smtp.gmail.com', 587)  # creates SMTP session
        s.starttls()  # start TLS for security
        s.login(strGmailSenderEmail, strGmailSenderPassword)  # Authentication
        for emailToSendTo in strEmailsToNotify:  # Send email to each person
            m = MIMEText(strEmailUpdatedMessage)
            m['Subject'] = strEmailSubjectPlural
            if len(elementDateButtons) == 1:
                m['Subject'] = strEmailSubjectSingular
            m['From'] = strGmailSenderEmail
            m['To'] = emailToSendTo   # Change the receiving email each time
            s.sendmail(strGmailSenderEmail, emailToSendTo, m.as_string())  # sending the mail
            if boolPrintEmailSentToEachPerson:
                print(colored(strEmailSentTo, colorEmailSentTo) + " " + emailToSendTo)
        s.quit()  # terminating the session
    if boolPrintProgramDone:
        print(colored("Program completed.", colorProgramDone))


if __name__ == "__main__":
    main()
