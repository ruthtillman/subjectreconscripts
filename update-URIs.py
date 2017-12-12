#!/usr/bin/env python
# Why does this script exist? This script exists so that we can work separately with ASpace data, create a spreadsheet (CSV) of the IDs of subjects which should be updated to include any authority_id but really probably a URI, and then rewrite downloads of those subjects as JSON files. The data to create this sheet and the JSON downloading info should be done separately. The data will probably come from MySQL queries. The downloads will probably come from a bash file. The bash file may then be called upon to run this Python script after using the same CSV to download the appropriate JSON files.

import os, requests, json, logging, csv, ConfigParser

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

# authenticates the session
auth = requests.post('{baseURL}/users/{user}/login?password={password}&expiring=false'.format(**dictionary)).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session}

def update_log(logStatus, uri,jsonFile,logFile):
    # It may eventually be useful to write a script which takes the beginning of the ALREADY EXISTS and does a check on those files to get the actual values to ensure it's not blank or otherwise a bad authority.
    if logStatus == 1:
        log = "SUCCESS: " + jsonFile + " updated to include " + uri + " and new file new-" + jsonFile + " created.\n"
    if logStatus == 0:
        log = "ALREADY EXISTS: " + jsonFile + " already contains a value for authority_id and" + uri + " was not added.\n"
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

def read_CSV(csvName,logFile):
    with open(csvName, newline='') as data:
        reader = csv.DictReader(data)
        for row in reader:
            write_URI(row['id'],row['uri'],logFile)

csvName = input("Enter the CSV name: ")
logFile = input("Enter the log file name: ")

read_CSV(csvName,logFile)



ASpaceHeader = "X-ArchivesSpace-Session:" + $SESSION

SESSION = input("Enter the ASpace session key: ")
