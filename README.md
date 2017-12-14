# Subject Reconciliation Scripts

These are Python3 scripts to be used for a local project to handle necessary subject work in our ArchivesSpace. Desired tasks include:

* Using ASpace subject IDs and subject URIs in an ingested CSV, download subject records, insert URIs, and post them back via the API.
* Create new ASpace subjects using data from a CSV.
* Using ASpace subject IDs and resource IDs, download the resource, test to see if the subjects are already referenced, and add them if they're not referenced, then post them back via the API.

Possible additional functions:

* Update titles or terms in existing subjects.
* Update other aspects of existing subjects.
* Add genres & non-topical subjects (ASpace's vocab for this is not great)

## Using the config file

This repository contains a file local_settings_model.cfg, which is a model of the local_settings.cfg file referenced by these scripts. The values for each entry follow the entry's declaration and colon without any spacing. For example, if admin username is "ArchivesWizzard," the row should appear as:

```
user:ArchivesWizzard
```

For security, modify this to fit your own values, save to a file `local_settings.cfg` in the project's root directory and do not commit/upload outside your institution.

baseURL *should end in a /* in order to be used properly throughout the script. Test to be sure it worker properly.

## External work

This project will also involve work querying the MySQL database to create a lot of the data which will actually go into the CSVs. It will include OpenRefine work in order to reconcile things with MARC records and perform other cleanup. It may include a directory of SQL queries and a directory of OpenRefine markdown files in order to document this work and keep it together.
