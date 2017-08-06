import json


def read_input_file():
    """Read Spotify uri input file and return array of corresponding ids"""
    with open('uri_input.txt', 'r') as f:
        ids = [line.rstrip('\n').split(':')[2] for line in f.readlines()]

    return ids


def write_to_file(objects, file_name, text=False):
    """Write the objects in `objects` as jsons to file `file_name`, or write text if `text` is True"""
    assert objects, "No objects passed to `write_to_file`"

    with open(file_name, 'w') as out_file:
        out_file.writelines([obj+'\n' if text else json.dumps(obj)+'\n' for obj in objects])
        print "Saved to {0}".format(file_name)

    pass
