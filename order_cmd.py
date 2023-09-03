#
# Order collection command.
# order <collection> on <attribute>
#

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

    collection.sort(id, False)


