import requests, csv, os, time, furls

# Steps to take:
# if thing.response_code == 200:
#  subject = thing.headers['X-Uri']
#  confirmLabel = thing.headers['X-Preflabel']
#  write these into the CSV

# for url, build instead using furls and escape using furls. Note we'll need to combine the initial `authorities/subjects/label/` and the subject when escaping.
#>>> subject = 'World War, 1939-1945--Personal narratives, American'
#>>> subpath = 'authorities/subjects/label/'
#>>> f = furl('http://id.loc.gov/')
#>>> f.path = subpath + subject
#>>> f.url
#'http://id.loc.gov/authorities/subjects/label/World%20War,%201939-1945--Personal%20narratives,%20American'
#>>> requests.get(f.url).headers['X-PrefLabel']
#'World War, 1939-1945--Personal narratives, American'

def URI_escape(value):
  return value.replace(' -- ', '--').replace(' ', '%20').replace(',', '%2C').replace("'","%27").replace('(', '%28').replace(')', '%29')

def get_subject_URIs(writer,csvSource):
  with open(csvSource, newline='') as data:
    reader = csv.DictReader(data)
    for row in reader:
      subjectLabel = URI_escape(row['subject'])
      subjectURI = 'http://id.loc.gov/authorities/subjects/label/' + subjectLabel
      subjectResponse = requests.get(subjectURI)
      if subjectResponse.status_code == 200:
          writer.writerow({'ASpaceID': row['ASpaceID'], 'subject' : row['subject'], 'LC_URI' : subjectResponse.headers['X-Uri'], 'LC_Label': subjectResponse.headers['X-Preflabel']})
      else:
          writer.writerow({'ASpaceID': row['ASpaceID'], 'subject' : row['subject'], 'LC_URI' : '', 'LC_Label': ''})
      time.sleep(4)

def write_subject_csv(csvOutput,csvSource):
    fieldnames = ['ASpaceID', 'subject', 'LC_URI', 'LC_Label']
    with open(csvOutput, 'w', newline='') as outputFile:
        writer = csv.DictWriter(outputFile, fieldnames=fieldnames)
        writer.writeheader()
        get_subject_URIs(writer,csvSource)

csvOutput='recon-test/scl_recon_2020_01_07.csv'
csvSource='recon-test/scl_lcsh_2020_01_06.csv'

write_subject_csv(csvOutput,csvSource)
