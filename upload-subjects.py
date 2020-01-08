#!/usr/bin/env python

# Creating a script which will take all "new-" subjects created by update-URIs.py and upload them to ArchivesSpace.

import os, json, glob

from asnake.client import ASnakeClient
client = ASnakeClient()
client.authorize()

def upload_new_subjects(JSONSource,client):
    os.chdir(JSONSource)
    files = glob.glob("new-*.json")
    for jsonFile in files:
        subject = json.load(open(jsonFile))
        subject_id = jsonFile[4:-5]
        response = client.post("/subjects/" + subject_id, data=json.dumps(subject)).json()
        response

JSONSource=input("Enter the source directory of new JSON Files: ")
upload_new_subjects(JSONSource,client)
