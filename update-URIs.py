#!/usr/bin/env python

import os, requests, json, logging, ConfigParser, csv

# Check to be sure that the URI is empty
# Tasks:
# Handle session ID and ASpace API URI as params to pass to the script variables
# Open CSV and call function to handle its two variables
# Create function to work with the two variables (do this first and then the CSV?)
# Write scripts to download via cURL and then post back. (ok so figure out how cURL works in Python or shift over to bash)

logFile = "log.txt"


def update_log(logStatus, uri,jsonFile,logFile):
    with open(logFile, "a") as logging:
    if logStatus = "succcess":
        log = "URI " + uri + " added to " + jsonFile + " and new file created.\n"
    if logStatus = "error":
        log = "URI " + uri + " not added to " + jsonFile + ". The subject already contains an authority_id value.\n"
    logging.write(log)

def write_URI(subject_id,uri,logFile):
    jsonFile = str(subject_id) + '.json'
    subject = json.load(open(jsonFile))
    if 'authority_id' not in subject:
        subject['authority_id'] = uri
        newJson = "new-" + jsonFile
        with open(newJson, "w") as outfile:
            json.dump(subject, outfile, sort_keys=True, indent=4)
        with open(logFile, "a") as logging:
            log = "URI " + uri + " added to " + newJson + "\n"
            logging.write(log)
    else:
        with open(logFile, "a") as logging:
            log = "URI " + uri + " not added to " + jsonFile + ". The subject already contains an authority_id value. \n"
            logging.write(log)
