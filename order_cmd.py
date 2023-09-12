#
# Order collection command.
# order <collection> on <attribute>
# order <collection> on <segment> <attribute>
# order <collection> on <segment1> with <segment2> on <attribute>
#

ORDER_ATT = 3
ORDER_SEG1 = 5
ORDER_SEG2 = 8

def order_collection(schema, command_line):
    # order <collection> on <attribute>
    if len(command_line) < 3:
        print("Invalid order command - too few arguments")
        return

    collection_name = command_line[1]
    print(collection_name)
    collection = schema.get_collection(collection_name)
    id = command_line[3]

    if collection is None:
        print("Invalid Collection")
        return

    # TODO check id
    # TODO more validation

    # Test bubble search and python list ordering algorithms.
    # TODO remove and use python list ordering, i.e., fast_sort
    if command_line[0] == "order":
        collection.sort(id, False)
    collection.fast_sort(id, False)

    order = len(command_line)
    if order == ORDER_ATT:
        pass
    elif order == ORDER_SEG1:
        pass
    elif order == ORDER_SEG2:
        pass
    else:
        pass


