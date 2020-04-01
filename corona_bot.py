import datetime
import json
import requests
import argparse
import logging
from bs4 import BeautifulSoup
from tabulate import tabulate
from slack_client import slacker

# Pythom time method asctime() converts a tuple or struct_
# time representing a time as returned by gmtime() or localtime() to a 24-character
# string of the following form: 'Tue Feb 17 23:21:05 2009'.
FORMAT = '[%(asctime)-15s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG, filename='bot.log', filemode='a')


URL = 'https://www.mohfw.gov.in/'
# This short_headers are the column of the table that have to be passed
SHORT_HEADERS = ['Sno', 'State','In','Fr','Cd','Dt']
FILE_NAME = 'corona_india_data.json'
# while calling the function from this declaration to anywhere
# else than the name will be extract_contents and/
#     extract_contents(row)
extract_contents = lambda row: [x.text.replace('\n', '') for x in row]

# this is the function to save the data to stringify format in json file
def save(x):
    with open(FILE_NAME, 'w') as f:
        json.dump(x, f)

def load():
    res={}
    with open(FILE_NAME, 'r') as f:
        res = json.load(f)
    return res

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--states', default=',')
    args = parser.parse_args()
    interested_states = args.states.split(',')
    current_time = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    info = []

    try:
        response = requests.get(URL).content
        soup = BeautifulSoup(response, 'html.parser')
        # print(soup.prettify())
        header = extract_contents(soup.tr.find_all('th'))
        print(header)
        stats = []
        all_rows = soup.find_all('tr')
        for row in all_rows:
            stat = extract_contents(row.find_all('td'))
            # print(stat)
            if stat:
                # remember the whole data comes in the end of the table where there is overall information
                # so here we are finding the last of the row with all stats whose length is 5
                if len(stat) == 5:

                   # print("this is the stat")
                    stats.append(stat)
                elif len(stat) == 4:
                    print(stat)
                    # append kiya idher '' for the last row
                    stat = ['', *stat]
                    stats.append(stat)

                    # print(stats)

                elif any([s.lower() in stat[1].lower() for s in interested_states]):
                    stats.append(stat)



        past_data=load()
        cur_data = {x[0]: {current_time: x[1:]} for x in stats}
        print(cur_data)

        print(cur_data)
    except Exception as e:
        logging.exception('oops, corono script failed.')
        slacker()(f'Exception occured: [{e}]')

