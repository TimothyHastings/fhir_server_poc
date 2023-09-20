"""
FHIR Server Proof of Concept
Author: Tim Hastings, 2023
"""

#
# loadUnique n <filename> into <collection>
# loadUnique 10000 PatientTemplate.fhir into Patient
# loadUnique 10000 ObservationTemplate.fhir into Observation
# Uses a template resource file that includes special characters
# ^ and | to do replacements of id and identifier value.
# TODO: Make the 'identifier value' random using a range that is 50% so there may be duplicates
#
from resource import Resource

def load_unique(schema, command_line):

    if not len(command_line) == 5:
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

        # Do the id and identifier replacements with the next value
        # id
        replace(resource, "^", str(i+1))
        # TODO make this a random number in a smaller range so we get duplicates
        # identifier value
        replace(resource, "|", str(i+1000))

        # Save the resource to the file system and in memory collection.
        resource.save()
        collection.add_resource(resource)

#
#   Replace a character in the FHIR
#   string replace will not work for some reason!
#
def replace(resource, a, b):
    l = len(resource.data)
    temp = ""
    for i in range(l):
        if resource.data[i] == a:
            temp += b
        else:
            temp += resource.data[i]
    resource.data = temp
