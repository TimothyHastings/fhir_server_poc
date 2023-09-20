"""
FHIR Server Proof of Concept
Author: Tim Hastings, 2023
"""

#
# selectParallel <qualifier> from <collection> where <attribute> <operator> <value>
# selectParallel distinct from Patient where id = 700
# Compare to:
# selectDistinct from Patient where id = 700
# selectParallel <qualifier> from <collection> where <segment> <attribute> <operator> <value>
#
# TODO: handle all qualifiers - currently jys distinct.
# TODO: handle N interleaves to determine optimal parallelism.
#

def select_parallel(schema, command_line):
    if not len(command_line) == 8:
        print("Invalid number of arguments")
        return
    qualifier = command_line[1]
    collection_name = command_line[3]
    collection = schema.get_collection(collection_name)

    if collection is None:
        print("Invalid Collection")
        return

    result = schema.get_collection("Result")
    if result is None:
        print("Result collection does not exist")

    attribute = command_line[5]
    operator = command_line[6]
    value = str(command_line[7])
    half = len(collection.resources) // 2
    resources = collection.resources
    for i in range(half):
        if str(resources[i].get_attribute_value(attribute)) == value:
            print(resources[i])
            result.resources.append(resources[i])
            if qualifier == "distinct":
                return
        if str(resources[i + half].get_attribute_value(attribute)) == value:
            print(resources[i + half])
            result.resources.append(resources[i + half])
            if qualifier == "distinct":
                return
