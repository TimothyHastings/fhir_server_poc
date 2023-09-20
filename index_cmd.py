"""
FHIR Server Proof of Concept
Author: Tim Hastings, 2023
"""
#
# Create and index using a dictionary on Collection.
# index <collection> on <attribute>
# index <collection> on <segment> <attribute>
#
def create_index(schema, command_line):
    collection_name = command_line[1]
    collection = schema.get_collection(collection_name)

    if collection is None:
        print("Invalid Collection")
        return
    if not command_line[2] == "on":
        print("Invalid qualifier")
        return

    # Clear the dictionary
    collection.catalogue = dict()
    if len(command_line) == 4:
        # index <collection> on <attribute>
        attribute = command_line[3]
        for resource in collection.resources:
            # Note keys are strings
            collection.catalogue[str(resource.get_attribute_value(attribute))] = resource.uuid
    elif len(command_line) == 5:
        # index <collection> on <segment> <attribute>
        segment = command_line[3]
        attribute = command_line[4]
        for resource in collection.resources:
            collection.catalogue[resource.get_segment_attribute_value(segment, attribute)] = resource.uuid
    else:
        print("Invalid number of arguments")

#
# selectIndex <qualifier> from <collection> where <attribute> <operator> <value>
# selectIndex <qualifier> from <collection> where <segment> <attribute> <operator> <value
#
def select_index(schema, command_line):
    collection_name = command_line[3]
    collection = schema.get_collection(collection_name)

    if collection is None:
        print("Invalid Collection")
        return

    if len(command_line) == 8:
        # selectIndex <qualifier> from <collection> where <attribute> <operator> <value>
        attribute = command_line[5]
        value = command_line[7]
        try:
            uuid = collection.catalogue[value]
        except Exception:
            print("Cannot find item in catalogue")
            return
        # Use the uuid to get the resource
        for resource in collection.resources:
            if resource.uuid == uuid:
                print(resource)
    elif len(command_line) == 9:
        # selectIndex <qualifier> from <collection> where <segment> <attribute> <operator> <value
        segment = command_line[5]
        attribute = command_line[6]
        value = command_line[8]
        try:
            uuid = collection.catalogue[value]
        except Exception:
            print("Cannot find item in catalogue")
            return
        # Use the uuid to get the resource
        for resource in collection.resources:
            if resource.uuid == uuid:
                print(resource)
    else:
        print("Invalid number of arguments")
