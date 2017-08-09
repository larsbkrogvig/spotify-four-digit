import constants
import util


def run():
    """Do first-time setup before running other actions"""
    ids = util.read_input_file()
    util.write_to_file(ids, "{}/tracks.txt".format(constants.PATH_IDS), text=True)
