import argparse
import utils


def main():
    parser = argparse.ArgumentParser()

    # positional arguments
    parser.add_argument('username',
                        action='store',
                        help='last.fm username')
    parser.add_argument('outfile',
                        action='store',
                        help='csv output file name')

    # optional arguments
    parser.add_argument('--quiet', action='store_true',
                        help='no verbose')
    parser.add_argument('--start', action='store',
                        help='first page to be fetched',
                        type=int)
    parser.add_argument('--end', action='store',
                        help='last page to be fetched',
                        type=int)
    parser.add_argument('--delimiter', action='store',
                        help='csv delimiter')

    arguments = parser.parse_args()

    # process parameters
    verbose = not arguments.quiet
    last_page = utils.get_last_page(arguments.username)

    if arguments.delimiter == None:
        delimiter = ';'
    else:
        delimiter = arguments.delimiter

    if arguments.end == None:
        end_page = last_page
    else:
        end_page = arguments.end

    if arguments.start == None:
        start_page = 1
    else:
        if arguments.start > end_page:
            raise ValueError(
                'provided starting page number is greater than the last page number.')
        else:
            start_page = arguments.start

    if verbose:
        print('importing the scrobbles of user {}'.format(arguments.username))
        print('starting page number: {}'.format(start_page))
        print('last page number: {}'.format(end_page))

    artists, songs, dates, times = utils.get_scrobbles(arguments.username,
                                                       start_page,
                                                       end_page,
                                                       verbose)
    utils.export_scrobbles_to_csv(artists, songs, dates, times,
                                  arguments.outfile,
                                  delimiter)

if __name__ == '__main__':
    main()
