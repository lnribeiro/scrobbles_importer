from lxml import html
from dateutil.relativedelta import relativedelta
import datetime
import requests
import csv

def process_timestamp(timestamp, now=None):
    if now == None:
        now = datetime.datetime.now()
    
    timestamp_split = timestamp.split()
    
    if timestamp_split[1] == 'minute' or \
       timestamp_split[1] == 'minutes' or \
       timestamp_split[1] == 'hour' or \
       timestamp_split[1] == 'hours':

           minutes = 0
           hours = 0
           # Ex: 'a minute ago' 
           if timestamp_split[1] == 'minute':
               minutes = 1
           # Ex: '4 minutes ago'
           if timestamp_split[1] == 'minutes':
               minutes_str = timestamp_split[0]
               minutes = int(minutes_str)
           # Ex: 'an hour ago' 
           if timestamp_split[1] == 'hour':
               hours = 1
           # Ex: '10 hours ago'
           if timestamp_split[1] == 'hours':
               hours_str = timestamp_split[0]
               hours = int(hours_str)
              
           delta = relativedelta(minutes=minutes,hours=hours)
           timestamp_date = now-delta
    else:
        # Ex: '12 Sep 12:34pm'
        if len(timestamp_split) == 3:
            # insert current year in the timestamp
            timestamp_split.insert(2,str(now.year)) 
            timestamp = ' '.join(timestamp_split)
            timestamp_date = datetime.datetime.strptime(timestamp,'%d %b %Y %I:%M%p')   
        # Ex: '10 Nov 2015, 6:12pm'
        elif len(timestamp_split) == 4:
            timestamp_date = datetime.datetime.strptime(timestamp,'%d %b %Y, %I:%M%p')       
        else:
            return -1 # error
            
    date_str = timestamp_date.strftime('%d/%m/%y')
    time_str = timestamp_date.strftime('%H:%M')               

    return date_str, time_str


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
    dates = []
    times = []
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
        for timestamp in map(process_timestamp, scrobbles_timestamps):
            dates.append(timestamp[0])
            times.append(timestamp[1])

        page_counter += 1
        
        if verbose:
            print(' OK!')

    return artists, songs, dates, times


def export_scrobbles_to_csv(artists, songs, dates, times, filename='scrobbles.csv', delimiter=';'):
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter)
        for record in zip(artists, songs, dates, times):
            writer.writerow(record)
