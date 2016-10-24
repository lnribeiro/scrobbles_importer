scrobbles_importer
==================

* A simple last.fm scrobbles importer. *


usage: scrobbles_importer.py [-h] [-u USER] [-o OUTFILE] [-v VERBOSE]
                             [-p LAST] [-s START] [-d DELIMITER]

arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  last.fm user
  -o OUTFILE, --outfile OUTFILE
                        name of the output .csv file
  -v VERBOSE, --verbose VERBOSE
                        verbose: True or False
  -p LAST, --pages LAST
                        number of pages to fetch
  -s START, --start START
                        first page to be fetched
  -d DELIMITER, --delimiter DELIMITER
                        csv delimiter
