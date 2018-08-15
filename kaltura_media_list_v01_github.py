# Python 3 Script to obtain list of all Kaltura media entries including title, ID and owner

import requests # needed for API requests
import json # needed to format results for display or export
import os # needed to clear screen for new output each time program run
import csv # needed to read/write csv files
import datetime # needed to nicely format dates

# Clear console for status messages
os.system('cls' if os.name == 'nt' else 'clear')

# Download media list
def download_kaltura_media_list():

    baseUrl = 'http://www.kaltura.com/api_v3/index.php?service=media&action=list&ks='
    # Obtain sessionId from http://www.kaltura.com/api_v3/testme/# - use
    # https://knowledge.kaltura.com/how-start-kaltura-session-using-testme-console
    # for instructions; use https://developer.kaltura.com/console/service/media/action/list
    # to test request and see results
    sessionId = '<INSERT SESSION VARIABLE HERE>'
    pagerUrl = '&format=1&pager[pageSize]=500&pager[pageIndex]='

    url = '%s%s%s' % (baseUrl, sessionId, pagerUrl)

    for page in range (1, 11):

        fullUrl = url + str(page)
        r = requests.get(fullUrl)
        data = json.loads(r.content)
        print ('Processing page ' + str(page))

        listLength = len(data['objects'])
        filename = 'Kaltura_Media_Export_File_' + datetime.datetime.now().strftime('%Y%m%d_%H%M') + '.csv'

        f = open(filename, 'a')
        f.write('title,collection_name,collection_owner,source,data_url,legacy_media_id, tags, description\n')

        i = 0
        while i < listLength:
            # To handle sometimes missing description
            try:
                (data['objects'][i]['description'])
                description = ((data['objects'][i]['description']).replace(',', ' '))
            except:
                description = ''

            f.write (
                (data['objects'][i]['name']).replace(',', ' ') + ',' +
                (data['objects'][i]['creatorId']).split('@', 1)[0] + ',' +
                (data['objects'][i]['creatorId']) + ',' +
                (data['objects'][i]['downloadUrl']) + ',' +
                (data['objects'][i]['dataUrl']) + ',' +
                (data['objects'][i]['id']) + ',' +
                '' + ',' +  # Leave tags blank
                description.replace('\n', ' ').replace('\r', ' ') +
                '\n' )
            i+=1
    f.close
    print ('Processing complete.')

download_kaltura_media_list()
