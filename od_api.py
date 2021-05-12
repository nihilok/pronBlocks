import requests
import json

app_id = 'cc2a92a7'
app_key = '0ed75d7d62b9eabd0231cbaadef1f995'

language = 'en-gb'
word_id = 'Cat'
fields = 'registers,domainClasses,pronunciations'
strictMatch = 'false'

def get_word_info(word):
    url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' + language + '/' + word.lower() + '?strictMatch=' + strictMatch  # + '?fields=' + fields + '&strictMatch=' + strictMatch;
    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
    return r

def get_pron(word):
    r = get_word_info(word).json()
    # print(len(r.json()['results']))
    if r.get('results'):
        pron = (r['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0]['phoneticSpelling'],
                '(' + r['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0]['dialects'][0] + ')')
        audio_url = r['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0]['audioFile']
        return pron, audio_url

if __name__ == '__main__':
    print(get_pron('turkey'))