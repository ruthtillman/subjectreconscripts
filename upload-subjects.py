#!/usr/bin/env python

# Creating a script which will take all "new-" subjects created by update-URIs.py and upload them to ArchivesSpace.

import os, requests, glob, json, logging, csv, configparser, datetime

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

def update_log(resultsGroup,logName,jobStart,jobEnd):
    # The log is created incrimentally because json.loads runs into various issues with these variables, so it's more straightforward to just add
    log = json.loads('{"jobType" : "upload_subjects"}')
    log['user'] = dictionary['user']
    log['dateTimeStart'] = jobStart
    log['dateTimeEnd'] = jobEnd
    log['responses'] = resultsGroup
    with open(logName, "a") as logging:
        json.dump(log, logging, indent=4)

def upload_new_subjects():
    files = glob.glob("new-*.json")
    logName = datetime.datetime.now().strftime('%Y-%m-%d-T-%H-%M') + "_subject_upload_log.json"
    jobStart = datetime.datetime.now().isoformat()
    results = []
    for jsonFile in files:
        subject = json.load(open(jsonFile))
        subject_id = jsonFile[4:-5]
        posts = requests.post(subjectBaseURL + subject_id, data=json.dumps(subject), headers=headers).json()
        posts['update_time'] = datetime.datetime.now().isoformat()
        results.append(posts)
    jobEnd = datetime.datetime.now().isoformat()
    update_log(results,logName,jobStart,jobEnd)

upload_new_subjects()
