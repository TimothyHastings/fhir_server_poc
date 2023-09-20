"""
FHIR Server Proof of Concept
Author: Tim Hastings, 2023
"""
#
# Order collection command.
# order <collection> on <attribute>
# order <collection> on <segment> <attribute>
#

ORDER_ATT = 3
ORDER_SEG1 = 4
ORDER_SEG2 = 7

def order_collection(schema, command_line):
    # order <collection> on <attribute>
    if len(command_line) < 3:
        print("Invalid order command - too few arguments")
        return
    if not command_line[2] == "on":
        print("Invalid order command - missing on qualifier")
        return

    collection_name = command_line[1]
    collection = schema.get_collection(collection_name)

    reverse = False
    if command_line[0] == "orderReverse":
        reverse = True

    if collection is None:
        print("Invalid Collection")
        return

    order = len(command_line) - 1

    if order == ORDER_ATT:
        # order <collection> on <attribute>
        attribute = command_line[3]
        collection.order_attribute(attribute, reverse)
    elif order == ORDER_SEG1:
        # order <collection> on <segment> <attribute>
        segment = command_line[3]
        attribute = command_line[4]
        collection.order_segment_attribute(segment, attribute, reverse)
    elif order == ORDER_SEG2:
        # order <collection> on <segment1> with <segment2> on <attribute>
        # TODO
        pass
    else:
        print("Invalid order command - too many arguments")


