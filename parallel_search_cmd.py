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
# This is a simulation of parallel process using interleaving simulating 4 processes.
# Additional process may improve the performance where t = On + Delta
# However, there is an optimal point where the additional overheads (Delta) make performance worse.
# This needs further investigation.
# Threading may be an option.
# However, threading may not provide performance improvement over interleaving.
# In addition a threading model must stop all threads for a distinct qualifier.
#

def select_parallel(schema, command_line):
    if len(command_line) >= 8:
        qualifier = command_line[1]
        collection_name = command_line[3]
        collection = schema.get_collection(collection_name)

        if collection is None:
            print("Invalid Collection")
            return

        result = schema.get_collection("Result")
        if result is None:
            print("Result collection does not exist")

    if len(command_line) == 8:
        # selectParallel distinct from Patient where id = 700
        attribute = command_line[5]
        operator = command_line[6]
        value = str(command_line[7])

        quarter = len(collection.resources) // 4
        half = len(collection.resources) // 2
        three_quarters = quarter + half
        resources = collection.resources
        for i in range(quarter):
            if str(resources[i].get_attribute_value(attribute)) == value:
                print(resources[i])
                result.resources.append(resources[i])
                if qualifier == "distinct":
                    print("Found in 1")
                    return
            if str(resources[i + quarter].get_attribute_value(attribute)) == value:
                print(resources[i + quarter])
                result.resources.append(resources[i + quarter])
                if qualifier == "distinct":
                    print("Found in 2")
                    return
            if str(resources[i + half].get_attribute_value(attribute)) == value:
                print(resources[i + half])
                result.resources.append(resources[i + half])
                if qualifier == "distinct":
                    print("Found in 3")
                    return
            if str(resources[i + three_quarters].get_attribute_value(attribute)) == value:
                print(resources[i + three_quarters])
                result.resources.append(resources[i + three_quarters])
                if qualifier == "distinct":
                    print("Found in 4")
                    return
    elif len(command_line) == 9:
        # selectParallel <qualifier> from <collection> where <segment> <attribute> <operator> <value>
        segment = command_line[5]
        attribute = command_line[6]
        operator = command_line[7]
        value = str(command_line[8])

        quarter = len(collection.resources) // 4
        half = len(collection.resources) // 2
        three_quarters = quarter + half
        resources = collection.resources
        for i in range(quarter):
            if str(resources[i].get_segment_attribute_value(segment, attribute)) == value:
                print(resources[i])
                result.resources.append(resources[i])
                if qualifier == "distinct":
                    print("Found in 1")
                    return
            if str(resources[i + quarter].get_segment_attribute_value(segment, attribute)) == value:
                print(resources[i + quarter])
                result.resources.append(resources[i + quarter])
                if qualifier == "distinct":
                    print("Found in 2")
                    return
            if str(resources[i + half].get_segment_attribute_value(segment, attribute)) == value:
                print(resources[i + half])
                result.resources.append(resources[i + half])
                if qualifier == "distinct":
                    print("Found in 3")
                    return
            if str(resources[i + three_quarters].get_segment_attribute_value(segment, attribute)) == value:
                print(resources[i + three_quarters])
                result.resources.append(resources[i + three_quarters])
                if qualifier == "distinct":
                    print("Found in 4")
                    return
    else:
        print("Invalid number of arguments")