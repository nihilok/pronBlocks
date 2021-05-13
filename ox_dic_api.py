import logging
import requests
from requests.exceptions import ConnectionError

logger = logging.getLogger('pronBlocks')
app_id = '<APP ID (Oxford Dictionary)>'
app_key = '<APP KEY>'

language = 'en-gb'
word_id = 'Cat'
fields = 'registers,domainClasses,pronunciations'
strictMatch = 'false'


def get_word_info(word):
    url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' + language + '/' + word.lower() + '?strictMatch=' + strictMatch  # + '?fields=' + fields + '&strictMatch=' + strictMatch;
    try:
        r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
        return r
    except ConnectionError as e:
        logger.error('Connection Error')
        return {}


def get_pron(word):
    r = get_word_info(word)
    r = r.json() if r else {}
    if r.get('results'):
        pron = (r['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0]['phoneticSpelling'],
                '(' + r['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0]['dialects'][0] + ')')
        audio_url = r['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0]['audioFile']
        return pron, audio_url

if __name__ == '__main__':
    print(get_pron('turkey'))