from lxml import html
import requests
import csv


def get_last_page(user):
    last_page = requests.get('http://www.last.fm/user/{}/library?page=99999'.format(user))
    last_page_node_tree = html.fromstring(last_page.content)
    return get_page_from_header(last_page_node_tree)


def get_page_from_header(node_tree):
    query = node_tree.xpath('//link[@rel="canonical"]/@href')
    address = query[0]
    address_length = len(address)
    equal_sign_pos = address.find('=')
    return int(address[-(address_length-equal_sign_pos-1):])


def get_scrobbles(user, start_page=1, end_page=5, verbose=False):
    artists = []
    songs = []
    timestamps = []
    page_counter = 1
    page_total = end_page-start_page+1

    for page_number in range(start_page, end_page+1):
        if page_number > end_page:
            break

        if verbose:
            print('Fetching page {}/{}...'.format(page_counter, page_total),end='')

        path = 'http://www.last.fm/user/{}/library?page={}'.format(user, page_number)
        page = requests.get(path)
        tree = html.fromstring(page.content)

        # process DOM tree using xpath to extract the desired information
        scrobbles_artists = tree.xpath('//span[@class="chartlist-artists"]/a/text()')
        scrobbles_songs = tree.xpath('//span[@class="chartlist-ellipsis-wrap"]/a/text()')
        scrobbles_timestamps = tree.xpath('//td[@class="chartlist-timestamp"]/span/text()')

        artists.extend(scrobbles_artists)
        songs.extend(scrobbles_songs)
        timestamps.extend(scrobbles_timestamps)

        page_counter += 1
        
        if verbose:
            print(' OK!')

    return artists, songs, timestamps


def export_scrobbles_to_csv(art, song, time, filename='scrobbles.csv', delimiter=';'):
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter)
        writer.writerow(['artist', 'song', 'timestamp'])
        for z in zip(art, song, time):
            writer.writerow(z)
