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
            collection.catalogue[str(resource.get_segment_attribute_value(segment, attribute))] = resource.uuid
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

    qualifier = command_line[1]

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
                print_result(qualifier, resource)
                break
    elif len(command_line) == 9:
        # selectIndex <qualifier> from <collection> where <segment> <attribute> <operator> <value>
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
                print_result(qualifier, resource)
                break
    else:
        print("Invalid number of arguments")

#
#
#
def print_result(qualifier, resource):
    if qualifier == "*":
        print(resource)
    elif qualifier == "distinct":
        print(resource)
    elif qualifier == "id":
        print(resource.uuid)
    elif qualifier == "data":
        print(resource.data)
    elif qualifier == "count":
        print("1")  # there can only be 1
    else:
        print("Unsupported qualifier")


#
# Display a collection's catalogue.
# showCat n <collection>
#
def show_catalogue(schema, command_line):
    if len(command_line) != 3:
        print("Invalid number of arguments")
        return

    collection_name = command_line[2]
    collection = schema.get_collection(collection_name)

    if collection is None:
        print("Invalid Collection")
        return

    # Test n is a number.
    try:
        n = int(command_line[1])
    except Exception:
        print("Invalid n - not an integer")
        return

    catalogue = collection.catalogue
    i = 0
    for k, v in catalogue.items():
        print(k, v)
        i += 1
        if i >= n:
            break

