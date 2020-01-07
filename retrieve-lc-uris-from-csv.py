import requests, csv, os

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

def URI_escape(value):
  return value.replace(' -- ', '--').replace(' ', '%20').replace(',', '%C').replace("'","%27").replace('(', '%28').replace(')', '%29')

def get_subject_URIs(writer,csvSource):
  with open(csvSource, newline='') as data:
    reader = csv.DictReader(data)
    for row in reader:
      subjectLabel = URI_escape(row['subject'])

def write_subject_csv(csvOutput,csvSource):
    fieldnames = ['ASpaceID', 'subject', 'LC_URI', 'LC_Label']
    with open(csvName, 'w', newline='') as outputFile:
        writer = csv.DictWriter(outputFile, fieldnames=fieldnames)
        writer.writeheader()
        get_subject_URIs(writer,csvSource)

csvOutput='recon-test/scl_recon_2020_01_07.csv'
csvSource='recon-test/scl_lcsh_2020_01_06.csv'
