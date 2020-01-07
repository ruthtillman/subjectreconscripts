import requests, csv

# Steps to take:
# open CSV and read title
# html escape spaces
# query
# subjectURI = 'https://id.loc.gov/authorities/subjects/label/' + label
# thing = requests.get(subjectURI)
# if thing.response_code == 200:
#  subject = thing.headers['X-Uri']
#  confirmLabel = thing.headers['X-Preflabel']
#  write these into the CSV
