#!/usr/bin/env python
# Why does this script exist? This script exists so that we can work separately with ASpace data, create a spreadsheet (CSV) of the IDs of subjects which should be updated to include any authority_id but really probably a URI.
# This script configures a connection to ArchivesSpace, authenticates the session, and gets headers. It then opens the CSV to download subjects as JSON responses based on the ID. Next, it opens the CSV again, opens each of those JSON files, tests whether it already contains authority_id, and inserts one if it doesn't. It logs either way.
# A second script will use the same CSV to post those subject records back to the server. A second script is desireable so that spot-checking of the records may be completed before it's run. This could be done by combining and pausing this script, but time should be allowed.
# The data will probably come from MySQL queries.

import os, requests, json, logging, csv, configparser
import datetime

# Check to be sure that the URI is empty
# Tasks:
# Handle session ID and ASpace API URI as params to pass to the script variables
# Write scripts to download via cURL and then post back. (ok so figure out how cURL works in Python or shift over to bash)

# Sets up config stuff for validation. Borrowed from ArchivesSnake-linked Duke scripts

configFilePath = 'local_settings.cfg'
config = configparser.ConfigParser()
config.read(configFilePath)

# From Duke: URL parameters dictionary, used to manage common URL patterns

dictionary = {'baseURL': config.get('ArchivesSpace', 'baseURL'), 'repository':config.get('ArchivesSpace', 'repository'), 'user': config.get('ArchivesSpace', 'user'),'password': config.get('ArchivesSpace', 'password')}
baseURL = dictionary['baseURL']
repositoryBaseURL = '{baseURL}/repositories/{repository}/'.format(**dictionary)
subjectBaseURL ='{baseURL}/subjects/'.format(**dictionary)

# authenticates the session
auth = requests.post('{baseURL}/users/{user}/login?password={password}&expiring=false'.format(**dictionary)).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session}

# Adapt this to open the CSV and do the call based on subject base URLs [note, this involved editing to change from repository base URL although that should be stored for handling the updates for DIGITAL OBJECTS]
def download_subjects(csvName):
    with open(csvName, newline='') as data:
        reader = csv.DictReader(data)
        downloadLog = "subject_download_log.txt"
        with open(downloadLog, "a") as logging:
            for row in reader:
                results = (requests.get(subjectBaseURL + row['id'], headers=headers)).json()
                subjectFile = row['id'] + '.json'
                with open(subjectFile, 'w') as outfile:
                    json.dump(results, outfile, sort_keys=True, indent=4)
                log = datetime.datetime.now().isoformat() + "\t" + subjectFile + " downloaded\n"
                logging.write(log)

def update_log(logStatus, uri,jsonFile,logFile):
    # It may eventually be useful to write a script which takes the beginning of the ALREADY EXISTS and does a check on those files to get the actual values to ensure it's not blank or otherwise a bad authority.
    if logStatus == 1:
        log = datetime.datetime.now().isoformat() + "\tSUCCESS\t" + jsonFile + "\tupdated to include " + uri + " and file new-" + jsonFile + " created.\n"
    if logStatus == 0:
        log = datetime.datetime.now().isoformat() + "\tALREADY EXISTS\t" + jsonFile + "\talready contains a value for authority_id and " + uri + " was not added.\n"
    with open(logFile, "a") as logging:
        logging.write(log)

def write_URI(subject_id,uri,logFile):
    jsonFile = subject_id + '.json'
    subject = json.load(open(jsonFile))
    if 'authority_id' not in subject:
        subject['authority_id'] = uri
        newJson = "new-" + jsonFile
        with open(newJson, "w") as outfile:
            json.dump(subject, outfile, sort_keys=True, indent=4)
        update_log(1,uri,jsonFile,logFile)
    else:
        update_log(0,uri,jsonFile,logFile)

def process_CSV(csvName,logFile):
    with open(csvName, newline='') as data:
        reader = csv.DictReader(data)
        for row in reader:
            write_URI(row['id'],row['uri'],logFile)

csvName = input("Enter the CSV name: ")
logFile = input("Enter the log file name: ")

download_subjects(csvName)
process_CSV(csvName,logFile)
