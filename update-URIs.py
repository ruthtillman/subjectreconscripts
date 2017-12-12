#!/usr/bin/env python

import os, requests, json, logging, csv

# Check to be sure that the URI is empty
# Tasks:
# Handle session ID and ASpace API URI as params to pass to the script variables
# Open CSV and call function to handle its two variables
# Create function to work with the two variables (do this first and then the CSV?)
# Write scripts to download via cURL and then post back. (ok so figure out how cURL works in Python or shift over to bash)

def update_log(logStatus, uri,jsonFile,logFile):
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
