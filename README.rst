scrobbles_importer
==================

*A simple last.fm scrobbles importer.*


usage: scrobbles_importer.py [-h] [--quiet] [--start START] [--end END]
                             [--delimiter DELIMITER]
                             username outfile

positional arguments:
  username              last.fm username
  outfile               csv output file name

optional arguments:
  -h, --help            show this help message and exit
  --quiet               no verbose
  --start START         first page to be fetched
  --end END             last page to be fetched
  --delimiter DELIMITER
                        csv delimiter

