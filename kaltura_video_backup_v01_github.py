# Python 3 script to download Kaltura source videos based on a CSV with entry IDs

import requests # needed for API requests; requests module must be installed in python environment
import json # needed to format results for display or export
import os # needed to clear screen for new output each time program run
import csv # needed to read/write csv files
import time # needed for time delays
import urllib # needed for easier file downloads vs requests method
import datetime # needed to nicely format dates

# Clear console
os.system('cls' if os.name == 'nt' else 'clear')

# Function to download Kaltura media by Kaltura Entry ID
def download_kaltura_source(entry_id):

    # Kaltura generic URL to download source videos; this will redirect to specific object ID URL
    url = 'https://cdnapisec.kaltura.com/p/<KALTURA INSTANCE ID>/sp/<KALTURA INSTANCE ID>00/playManifest/entryId/%s/format/url/flavorParamId/0' % (entry_id)

    # Obtain the redirect URL and derive the file type to be downloaded
    r = requests.head(url, allow_redirects=True)
    print ('Status: ', r.status_code)

    # Error handling download valid files; record status codes to log file
    if r.status_code == 404:
        return r.status_code
    else:
        output_file_extension = r.url.split('/')[-1].split('?')[0].split('.')[1]
        output_filename = entry_id + '.' + output_file_extension
        print ('Downloading ' + output_filename, end='')

        # Download the media file in chunks
        response = requests.get(url, stream=True)
        handle = open(output_filename, "wb")
        total_size = format((int(response.headers.get('content-length'))/1024/1024), '.2f')
        print (' Size = ' + str(total_size) + 'MB')
        for chunk in response.iter_content(chunk_size=512):
            if chunk:  # filter out keep-alive new chunks
                handle.write(chunk)
        return r.status_code

# Load Kaltura Entry IDs from CSV and download source video
def read_kaltura_entry_ids():
    with open('Kaltura_Entry_IDs.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        filename = 'Kaltura_Download_Error_Log_' + datetime.datetime.now().strftime('%Y%m%d_%H%M') + '.csv'
        f = open(filename, 'w')
        f.write('%s, %s \n' % ('Kaltura Entry ID', 'Status'))
        for row in readCSV:
            if row[0] != 'entry_id':
                kaltura_entry_id = str(row[0])
                print ('Attempting Kaltura ID: ', kaltura_entry_id)
                status_code = download_kaltura_source(kaltura_entry_id)
                f.write('%s, %s \n' % (kaltura_entry_id, status_code))
        f.close

read_kaltura_entry_ids()
