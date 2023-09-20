FHIR Proof of Concept
Tim Hastings, 2023

Files:
cli.py                      Command Line Interface - processes SQL-like commands
collection.py               Defines a database collection class.
Commands.txt                List of commands used for help.
index.py                    Example database indexing.
loadUnique.py               Example loading fhir records using a FHIR template.
loader.py                   Loads collections from the file system.
main.py                     Creates and loads the database.
ObservationTemplate.fhir    Observation FHIR Template.
order_cms.py                Example order collection command.
parallel_search_cmd.py      Example parallel processing select command.
PatientTemplate.fhir        Patient FHIR Template.
query.py                    Underlying FHIR (json) queries.
resource.py                 Defines a basic resource used in the database.
schema.py                   Defines a database schema.
search_cmd.py               Example search command using a defined attribute.
test.txt                    Instructions to build a database and run sample tests.
test_cases.txt              Sample test case commands.


References:
https://www.hl7.org/fhir/index.html
For examples go to https://www.hl7.org/fhir/resourcelist.html
FHIR Server POC.pptx