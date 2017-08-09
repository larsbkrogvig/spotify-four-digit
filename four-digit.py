import getopt
import sys

import actions

VALID_ACTIONS = [
    'setup',
    'api_get',
    'bq_get_schema',
    'bq_upload',
    'bq_get_ids',
    'print_token'
]


def main(argv):

    args, sample = get_options_and_arguments(argv)

    action = args.pop(0)

    if action not in VALID_ACTIONS:
        print "Invalid action {}".format(action)
        print "Usage: four-digit.py [-s] [{0}]".format(' | '.join(VALID_ACTIONS))
        sys.exit(2)

    if action == 'setup':
        actions.setup.run()

    if action == 'api_get':
        actions.api_get.run(args, sample)

    if action == 'bq_get_schema':
        actions.bq_get_schema.run(args)

    if action == 'bq_upload':
        actions.bq_upload.run(args, sample)

    if action == 'bq_get_ids':
        actions.bq_get_ids.run(args, sample)

    pass


def get_options_and_arguments(argv):
    """Get options and arguments from user input, print usage help if invalid input"""

    try:
        opts, args = getopt.getopt(argv, 's', ['sample'])

        # Arguments
        if not args:
            raise getopt.GetoptError('No arguments given')

        # Options
        sample = False
        for opt, arg in opts:
            if opt in ("-s", "--sample"):
                sample = True
            else:
                raise getopt.GetoptError("Unknown option '{}'".format(opt))

    except getopt.GetoptError as err:

        print err, '\nUsage: four-digit.py [-s] [{0}] '.format('|'.join(VALID_ACTIONS))
        sys.exit(2)

    return args, sample


if __name__ == "__main__":
    main(sys.argv[1:])

