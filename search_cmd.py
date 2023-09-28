"""
FHIR Server Proof of Concept
Author: Tim Hastings, 2023

The Search commands implement a dynamic search Algorithm.
Commands to set the search attribute:
for <collection> add <attribute>
for <collection> add <segment> with <attribute>

Commands to search a collection:
search <collection> where <attribute> <operator> <value>
searchDistinct <collection> where <attribute> <operator> <value>

Examples:

for Patient100K add id
search * from Patient100K where id = 50000

for Patient add identifier with value
search * from Patient100K where identifier = 100000
"""
#
# Set a search attribute.
# for <collection> add <attribute>
# for <collection> add <segment> with <attribute>
#
def set_search_attribute(schema, command_line):
    collection_name = command_line[1]
    collection = schema.get_collection(collection_name)

    if collection is None:
        print("Invalid Collection")
        return
    if not command_line[2] == "add":
        print("Invalid qualifier")
        return

    if len(command_line) == 4:
        # for <collection> add <attribute>
        attribute = command_line[3]
        for resource in collection.resources:
            val = resource.get_attribute_value(attribute)
            if val is None:
                print("Invalid attribute")
                return
            resource.search_field = val

    elif len(command_line) == 6:
        # for <collection> add <segment> with <attribute>
        attribute = command_line[5]
        segment = command_line[3]
        for resource in collection.resources:
            val = resource.get_segment_attribute_value(segment, attribute)
            if val is None:
                print("Invalid attribute")
                return
            resource.search_field = val
    else:
        print("Invalid set search command")

#
# search <qualifier> from <collection> where <attribute> <operator> <value>
# Not required search <qualifier> from <collection> where <segment> <attribute> <operator> <value>
# This command is not needed as the search criteria is set by the for command.
#
def search_attribute(schema, command_line):
    collection_name = command_line[3]
    collection = schema.get_collection(collection_name)

    if collection is None:
        print("Invalid Collection")
        return

    if not command_line[4] == "where":
        print("Invalid qualifier")
        return

    distinct = False
    if command_line[1] == "distinct":
        distinct = True

    if len(command_line) == 8:
        # search <collection> where <attribute> <operator> <value>
        operator = command_line[6]
        value = command_line[7]
        for resource in collection.resources:
            if compare_attribute_value(resource.search_field, value, operator):
                print(resource)
                if distinct:
                    break
    else:
        print("Incorrect number of arguments")

#
#   Compare 2 values.
#   TODO Handle string comparisons.
#
def compare_attribute_value(att, val, operator):
    x = att
    if val.isnumeric():
        y = int(val)

    try:
        if operator == "=":
            return x == y
        if operator == "!=":
            return x != y
        elif operator == ">":
            return x > y
        elif operator == ">=":
            return x >= y
        elif operator == "<":
            return x < y
        elif operator <= y:
            return x <= y
        else:
            print("Invalid operator")
            return False
    except Exception:
        print("Bad comparison")
        return False