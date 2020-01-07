#!/usr/bin/env python
# Why does this script exist? This script exists so that we can work separately with ASpace data, create a spreadsheet (CSV) of the IDs of subjects which should be updated to include any authority_id but really probably a URI.
# This script configures a connection to ArchivesSpace, authenticates the session, and gets headers. It then opens the CSV to download subjects as JSON responses based on the ID. Next, it opens the CSV again, opens each of those JSON files, tests whether it already contains authority_id, and inserts one if it doesn't. It logs either way.
# A second script will use the same CSV to post those subject records back to the server. A second script is desireable so that spot-checking of the records may be completed before it's run. This could be done by combining and pausing this script, but time should be allowed.
# The data will probably come from MySQL queries.

import os, requests, json, logging, csv, configparser, datetime

# Check to be sure that the URI is empty
# Tasks:
# Handle session ID and ASpace API URI as params to pass to the script variables
# Write scripts to download via cURL and then post back. (ok so figure out how cURL works in Python or shift over to bash)

# Sets up config stuff for validation. Borrowed from ArchivesSnake-linked Duke scripts

configFilePath = 'local_settings.cfg'
config = configparser.ConfigParser()
config.read(configFilePath)

# From Duke: URL parameters dictionary, used to manage common URL patterns

dictionary = {'baseURL': config.get('ArchivesSpace', 'baseURL'), 'user': config.get('ArchivesSpace', 'user'),'password': config.get('ArchivesSpace', 'password')}
baseURL = dictionary['baseURL']
subjectBaseURL ='{baseURL}subjects/'.format(**dictionary)

# authenticates the session
auth = requests.post('{baseURL}/users/{user}/login?password={password}&expiring=false'.format(**dictionary)).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session}

# Opens the CSV which has been input by the user. Opens it as a CSV reader, starts a download log file and opens that to write the confirmations of what's been downloaded (this is not _true_ logging). For each row the CSV, send an API get request with already-generated headers based on the base API URL for subjects and the subject ID as taken from the id column of the CSV. Interprets response as JSON. Uses the same id to create a filename and dumps the JSON response into the file. Then writes a log entry presuming that the download was successful at the approx timestamp (note, it will be off by at most a second)... the assumption is that any breaks in the process will stop the log from being written but the errors won't be written to the log yet.

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

# Takes a set of inputs related to an action just performed and either writes a positive or negative status with those log values into the log. The tab-separation means this can be used in spreadsheet format (as TSV).

def update_log(logStatus, uri,jsonFile,logFile):
    if logStatus == 1:
        log = datetime.datetime.now().isoformat() + "\tSUCCESS\t" + jsonFile + "\tupdated to include " + uri + " and file new-" + jsonFile + " created.\n"
    if logStatus == 0:
        log = datetime.datetime.now().isoformat() + "\tALREADY EXISTS\t" + jsonFile + "\talready contains a value for authority_id and " + uri + " was not added.\n"
    with open(logFile, "a") as logging:
        logging.write(log)

# opens the JSON file for each subject record, loads it as a JSON object, tests to see if the file contains an authority_id field, if not it adds a new field with the value of the uri it received from process_CSV as its value. It then writes a new JSON file which uses the same identifier, but adds a pre-fix new. The function calls the logging function and passes on a status dependent on whether it found an authority_id and created a new file or not.

## These changes below need to be tested on files which contain blank or other such URIs before committing. Also ASpace needs to be tested to see if this is even an issue.

def write_URI(subject_id,uri,logFile):
    jsonFile = subject_id + '.json'
    subject = json.load(open(jsonFile))
    newJson = "new-" + jsonFile
    if subject.has_key('authority_id'):
        if subject['authority_id'] == '':
            subject['authority_id'] = uri
            write_subject_JSON(subject,newJson)
            update_log(1,uri,jsonFile,logFile)
        elif subject['authority_id'] == ' ':
            subject['authority_id'] = uri
            write_subject_JSON(subject,newJson)
            update_log(1,uri,jsonFile,logFile)
        else:
            update_log(0,uri,jsonFile,logFile)
    else:
        subject['authority_id'] = uri
        write_subject_JSON(subject,newJson)
        update_log(1,uri,jsonFile,logFile)


def write_to_JSON(content,newJson):
    with open(newJson, "w") as outfile:
        json.dump(content, outfile, sort_keys=True, indent=4)

# Opens the CSV which has been provided as input by the user, opens and passes to a CSV parser, and for each row calls the function to add test for and add authority_ids if they don't exist, passing along the values for the id column and URI column from the CSV along with the name of the log file for homebrewed logging purposes.

def process_CSV(csvName,logFile):
    with open(csvName, newline='') as data:
        reader = csv.DictReader(data)
        for row in reader:
            write_URI(row['id'],row['uri'],logFile)

csvName = input("Enter the CSV name: ")
logFile = input("Enter the log file name: ")

download_subjects(csvName)
process_CSV(csvName,logFile)
