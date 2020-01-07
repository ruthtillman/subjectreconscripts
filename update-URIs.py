#!/usr/bin/env python
# Why does this script exist? This script exists so that we can work separately with ASpace data, create a spreadsheet (CSV) of the IDs of subjects which should be updated to include any authority_id but really probably a URI.
# This script connects to ASpace It then opens the CSV to download subjects as JSON responses based on the ID (if a URI exists). Next, it opens the CSV again, opens each of those JSON files, tests whether it already contains authority_id, and inserts one if it doesn't.
# A second script will post subject records back to the server.

import os, json, csv, datetime

# Validate ASnake
from asnake.client import ASnakeClient
client = ASnakeClient()
client.authorize()

# Opens the CSV which has been input by the user. Opens it as a CSV reader. For each row the CSV which contains an LC ID, send an API get request with already-generated headers based on the base API URL for subjects and the subject ID as taken from the id column of the CSV. Interprets response as JSON. Uses the same id to create a filename and dumps the JSON response into the file.

def write_to_JSON(content,newJson):
    with open(newJson, "w") as outfile:
        json.dump(content, outfile, sort_keys=True, indent=4)

def download_subjects(csvName,client):
    with open(csvName, newline='') as data:
        reader = csv.DictReader(data)
        for row in reader:
            if row['LC_URI'] != '':
                subject = client.get('/subjects/' + row['ASpaceID'].json()
                subjectFile = 'recon-test/' + row['ASpaceID'] + '.json'
                write_to_json(subject,subjectFile)

# opens the JSON file for each subject record, loads it as a JSON object, tests to see if the file contains an authority_id field, if not it adds a new field with the value of the uri it received from process_CSV as its value. It then writes a new JSON file which uses the same identifier, but adds a pre-fix "new".

## These changes below need to be tested on files which contain blank or other such URIs before committing. Also ASpace needs to be tested to see if this is even an issue.

def write_URI(subject_id,uri):
    jsonFile = subject_id + '.json'
    subject = json.load(open(jsonFile))
    newJson = "new-" + jsonFile
    if subject.has_key('authority_id'):
        if subject['authority_id'] == '':
            subject['authority_id'] = uri
            write_to_JSON(subject,newJson)
        elif subject['authority_id'] == ' ':
            subject['authority_id'] = uri
            write_to_JSON(subject,newJson)
    else:
        subject['authority_id'] = uri
        write_to_JSON(subject,newJson)

# Opens the CSV which has been provided as input by the user, opens and passes to a CSV parser, and for each row calls the function to add test for and add authority_ids if they don't exist, passing along the values for the id column and URI column from the CSV along with the name of the log file for homebrewed logging purposes.

def process_CSV(csvName,logFile):
    with open(csvName, newline='') as data:
        reader = csv.DictReader(data)
        for row in reader:
            if row['LC_URI'] != '':
                write_URI(row['ASpaceID'],row['LC_URI'],logFile)

csvName = input("Enter the CSV name: ")
logFile = input("Enter the log file name: ")

download_subjects(csvName,client)
process_CSV(csvName,logFile)
