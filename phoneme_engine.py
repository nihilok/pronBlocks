import random
from random import randint
import requests
import re
from ursina import Audio, destroy, camera
import logging

from od_api import get_pron

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PhonemeEngine:
    sounds = {
        'æ': Audio('sounds/ae.mp3', autoplay=False),
        'm': Audio('sounds/m.mp3', autoplay=False),
        'b': Audio('sounds/b.mp3', autoplay=False),
        'j': Audio('sounds/j.mp3', autoplay=False),
        'ə': Audio('sounds/uh.mp3', autoplay=False),
        'l': Audio('sounds/l.mp3', autoplay=False),
        'n': Audio('sounds/n.mp3', autoplay=False),
        's': Audio('sounds/s.mp3', autoplay=False),
        'ɪ': Audio('sounds/i.mp3', autoplay=False),
        'h': Audio('sounds/h.mp3', autoplay=False),
        'f': Audio('sounds/f.mp3', autoplay=False),
        'g': Audio('sounds/g.mp3', autoplay=False),
        'i': Audio('sounds/ii.mp3', autoplay=False),
        'd': Audio('sounds/d.mp3', autoplay=False),
        'p': Audio('sounds/p.mp3', autoplay=False),
        't': Audio('sounds/t.mp3', autoplay=False),
        'z': Audio('sounds/z.mp3', autoplay=False),
        'u': Audio('sounds/u.mp3', autoplay=False),
        'r': Audio('sounds/r.mp3', autoplay=False),
        'v': Audio('sounds/v.mp3', autoplay=False),
        'w': Audio('sounds/w.mp3', autoplay=False),
        'k': Audio('sounds/k.mp3', autoplay=False),
        'ʊ': Audio('sounds/oo.mp3', autoplay=False),
        'ð': Audio('sounds/the.mp3', autoplay=False),
        'ɔ': Audio('sounds/or.mp3', autoplay=False),
        'θ': Audio('sounds/th.mp3', autoplay=False),
        'ʃ': Audio('sounds/sh.mp3', autoplay=False),
        'ʧ': Audio('sounds/ch.mp3', autoplay=False),
        'ɛ': Audio('sounds/e.mp3', autoplay=False),
        'ʒ': Audio('sounds/zi.mp3', autoplay=False),
        'e': Audio('sounds/e.mp3', autoplay=False),
        'o': Audio('sounds/o.mp3', autoplay=False),
        'ɒ': Audio('sounds/o.mp3', autoplay=False),
        'ɜ': Audio('sounds/ir.mp3', autoplay=False),
        'ŋ': Audio('sounds/ng.mp3', autoplay=False),
        'ʤ': Audio('sounds/dge.mp3', autoplay=False),
        'a': Audio('sounds/ai.mp3', autoplay=False),
        'ɑ': Audio('sounds/ar.mp3', autoplay=False),
        'ʌ': Audio('sounds/uhh.mp3', autoplay=False),
        'win': Audio('sounds/twang.mp3', autoplay=False),
        'lose': Audio('sounds/rasberry.mp3', autoplay=False),
    }

    textures = {
        'æ': 'textures/ae.png',
        'm': 'textures/m.png',
        'b': 'textures/b.png',
        'j': 'textures/j.png',
        'ə': 'textures/uh.png',
        'l': 'textures/l.png',
        'n': 'textures/n.png',
        's': 'textures/s.png',
        'ɪ': 'textures/i.png',
        'h': 'textures/h.png',
        'f': 'textures/f.png',
        'g': 'textures/g.png',
        'i': 'textures/ii.png',
        'd': 'textures/d.png',
        'p': 'textures/p.png',
        't': 'textures/t.png',
        'z': 'textures/z.png',
        'u': 'textures/u.png',
        'r': 'textures/r.png',
        'v': 'textures/v.png',
        'w': 'textures/w.png',
        'k': 'textures/k.png',
        'ʊ': 'textures/oo.png',
        'ð': 'textures/the.png',
        'ɔ': 'textures/or.png',
        'θ': 'textures/th.png',
        'ʃ': 'textures/sh.png',
        'ʧ': 'textures/ch.png',
        'ɛ': 'textures/e.png',
        'ʒ': 'textures/zi.png',
        'e': 'textures/e.png',
        'o': 'textures/uh.png',
        'ɒ': 'textures/o.png',
        'ɜ': 'textures/ir.png',
        'ŋ': 'textures/ng.png',
        'ʤ': 'textures/dge.png',
        'a': 'textures/ai.png',
        'ɑ': 'textures/ar.png',
        'ʌ': 'textures/uhh.png'
    }

    def __init__(self, words: list):
        self.words = words
        self.word = ''
        self.pron_response = get_pron(self.word) if self.word else None
        self.phonemes, self.original_phonemes = [], []
        self.full_audio_dict = {}

    # TODO: make the next 2 methods async and add fallback to web-scraping method:
    def pron(self):
        if self.pron_response:
            # data = {
            #     'text_to_transcribe': self.word,
            #     'submit': "Show+transcription",
            #     'output_dialect': 'br',
            #     'output_style': 'only_tr',
            #     'preBracket': '',
            #     'postBracket': '',
            #     'speech_support': '0'}
            #
            # response = requests.post('https://tophonetics.com/', data=data)
            #
            # for line in response.text.split('\n'):
            #     if line.startswith('<div id="transcr_output"><span class="transcribed_word">'):
            #         word_plus = line[len('<div id="transcr_output"><span class="transcribed_word">'):]
            #         pattern = r'^\w+'
            #         match = re.match(pattern, word_plus)
            #         if match:
            #             pron = match.group(0)
            #             logger.debug(f'Pron: {pron}')
            #             return pron
            # print(self.pron_response[0][0])
            return self.pron_response[0][0]
        return None

    def get_full_audio(self):
        # url = f"https://d1qx7pbj0dvboc.cloudfront.net/{self.word}.mp3"
        # params = {
        #     "headers": {
        #         "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0",
        #         "Accept": "audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5",
        #         "Accept-Language": "en-GB,en;q=0.5",
        #         "Range": "bytes=0-"
        #     },
        # }
        if self.pron_response:
            url = self.pron_response[1]
            response = requests.get(url) #, **params)
            file = response.content
            open(f'sounds/{self.word}.mp3', 'wb').write(file)
            self.full_audio_dict[self.word] = Audio(f'sounds/{self.word}.mp3')


    def get_phonemes(self):
        pron = self.pron()
        if pron:
            pron = pron.replace('ɛ', 'e')
            pron = pron.replace('əː', 'ɜː')
            pron = pron.replace('a', 'æ')
            pron = pron.replace('ɛː', 'eə')
            pron = pron.replace('ʌɪ', 'aɪ')
            pron = pron.replace('(ə)', '')
            original_phonemes = list(pron)
            if "'" in original_phonemes:
                original_phonemes.remove("'")
            if "," in original_phonemes:
                original_phonemes.remove(",")
            if 'ˈ' in original_phonemes:
                original_phonemes.remove('ˈ')
            if 'ː' in original_phonemes:
                original_phonemes.remove('ː')
            if 'ˌ' in original_phonemes:
                original_phonemes.remove('ˌ')
            phonemes = original_phonemes.copy()
            random.shuffle(phonemes)
            logger.debug(f'Original Phonemes: {original_phonemes}')
            logger.debug(f'Shuffled Phonemes: {phonemes}')
            return phonemes, original_phonemes
        return [], []

    def set_positions(self):
        self.test_positions = []
        return self.test_positions

    def set_up_word(self, index):
        self.word = self.words.pop(index)
        self.pron_response = get_pron(self.word)
        self.phonemes, self.original_phonemes = self.get_phonemes()
        self.set_positions()
        self.get_full_audio()

    def get_new_word(self):
        if len(self.words) > 1:
            index = randint(0, len(self.words) - 1)
            self.set_up_word(index)
        elif len(self.words) == 1:
            self.set_up_word(0)
        else:
            self.word = None
        return self.word
