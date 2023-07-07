from fastapi import FastAPI
import requests


app = FastAPI()

@app.get('/get-word/{word}')
def get_word(word: str):
    fetch_word = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/%s' % word)

    word_data = fetch_word.json()

    if isinstance(word_data, list):
        return word_data
    return word_data['title']

@app.get('/get-word-meaning/{word}')
def get_word(word: str):
    fetch_word = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/%s' % word)

    word_data = fetch_word.json()

    if isinstance(word_data, list):
        word_meanings = word_data[0]['meanings']

        word = []
        for part_of_speech in word_meanings:
            word_definitions = [{
                'definition': word['definition'],
                'example': word['example'] if 'example' in word else []
                } for word in part_of_speech['definitions']]
            word.append({'partOfSpeech': part_of_speech['partOfSpeech'], 'definitions': word_definitions})
        return word
    return word_data['title']
    

@app.get('/get-word-phonetics/{word}')
def get_word(word: str):
    fetch_word = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/%s' % word)

    word_data = fetch_word.json()
    if isinstance(word_data, list):
        word_phonetics = word_data[0]['phonetics']
        phonetic_list = []
        for phonetic in word_phonetics:
            if 'us' in phonetic['audio']:
                phonetic_list.append({'audio': phonetic['audio'], 'type': 'us'})
            if 'uk' in phonetic['audio']:
                phonetic_list.append({'audio': phonetic['audio'], 'type': 'uk'})
            if 'au' in phonetic['audio']:
                phonetic_list.append({'audio': phonetic['audio'], 'type': 'au'})

        return phonetic_list
    return word_data['title']