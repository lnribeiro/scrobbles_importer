import argparse
import utils


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user',
                        action='store', dest='user',
                        help='last.fm user')
    parser.add_argument('-o', '--outfile',
                        action='store', dest='outfile', default='scrobbles.csv',
                        help='name of the output .csv file')
    parser.add_argument('-v', '--verbose',
                        action='store', dest='verbose', default=True, type=bool,
                        help='verbose: True or False')
    parser.add_argument('-p', '--pages',
                        action='store', dest='last', default=5,
                        help='number of pages to fetch')
    parser.add_argument('-s', '--start', default=1,
                        action='store', dest='start',
                        help='first page to be fetched')
    parser.add_argument('-d', '--delimiter', default=';',
                        action='store', dest='delimiter',
                        help='csv delimiter')
    arguments = parser.parse_args()

    if arguments.user:
        artists, songs, timestamps = utils.get_scrobbles(arguments.user,
                                                         start_page=arguments.start,
                                                         end_page=arguments.last,
                                                         verbose=arguments.verbose)
        utils.export_scrobbles_to_csv(artists, songs, timestamps,
                                      filename=arguments.outfile,
                                      delimiter=arguments.delimiter)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
