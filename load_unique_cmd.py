"""
FHIR Server Proof of Concept
Author: Tim Hastings, 2023
"""

#
# loadUnique n <filename> into <collection> |duplicate|
# duplicate is optional to create identifier value duplicates.
# This is useful for a Patient having 1 or more Observations
# loadUnique 10000 PatientTemplate.fhir into Patient
# loadUnique 10000 ObservationTemplate.fhir into Observation
# Uses a template resource file that uses #tag replacements.
#
import random

from resource import Resource


def load_unique(schema, command_line):
    duplicate = False
    length = len(command_line)
    if length == 6:
        length -= 1
        if command_line[5] == "duplicate":
            duplicate = True
        else:
            print("Invalid option")
            return

    if not length == 5:
        print("Invalid number of arguments")
        return

    collection_name = command_line[4]
    collection = schema.get_collection(collection_name)

    if collection is None:
        print("Invalid Collection")
        return

    try:
        n = int(command_line[1])
    except Exception:
        print("Invalid n - not an integer")
        return

    file_name = command_line[2]

    if not command_line[3] == "into":
        print("Invalid argument")
        return
    # Clear the collections resources to avoid duplicate ids.
    # Add the unique resources by id and identifier.
    collection.resources = list()
    for i in range(n):
        # Create a new resource.
        resource = Resource(collection.name)
        if not resource.load_file(file_name, ""):
            print("Cannot find template file")
            return

        # identifier_value replacement - NOTE do this first to void #id replacement conflicts.
        # Option to replace with random duplicates.

        if duplicate:
            rn = random.randint(1, n // 2)
            replace(resource, "#identifier_value", str(1000 + rn))
        else:
            replace(resource, "#identifier_value", str(1000 + i+1))

        # id replacement
        # id is not part of FHIR and used as a unique number.
        replace(resource, "#id", str(i+1))

        # family_name example of how to replace other fields.
        replace(resource, "#name_family", "Family " + str(i+1))

        # Save the resource to the file system and in memory collection.
        resource.save()
        collection.add_resource(resource)


#
#   Replace a string - used for #tags
#   Note that the replace method return a new string.
#
def replace(resource, a, b):
    temp = resource.data.replace(a, b)
    resource.data = temp
