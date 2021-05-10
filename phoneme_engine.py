import random
from random import randint
import requests
import re
from ursina import Audio, destroy
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
        'æ': 'ae.png',
        'm': 'm.png',
        'b': 'b.png',
        'j': 'j.png',
        'ə': 'uh.png',
        'l': 'l.png',
        'n': 'n.png',
        's': 's.png',
        'ɪ': 'I.png',
        'h': 'h.png',
        'f': 'f.png',
        'g': 'g.png',
        'i': 'i.png',
        'd': 'd.png',
        'p': 'p.png',
        't': 't.png',
        'z': 'z.png',
        'u': 'u.png',
        'r': 'r.png',
        'v': 'v.png',
        'w': 'w.png',
        'k': 'k.png',
        'ʊ': 'oo.png',
        'ð': 'the.png',
        'ɔ': 'or.png',
        'θ': 'th.png',
        'ʃ': 'sh.png',
        'ʧ': 'ch.png',
        'ɛ': 'e.png',
        'ʒ': 'zi.png',
        'e': 'e.png',
        'o': 'uh.png',
        'ɒ': 'o.png',
        'ɜ': 'ir.png',
        'ŋ': 'ng.png',
        'ʤ': 'dge.png',
        'a': 'ai.png',
        'ɑ': 'ar.png',
        'ʌ': 'uhh.png'
    }

    def __init__(self, words: list):
        self.words = words
        self.word = ''
        self.phonemes, self.original_phonemes = [], []
        self.full_audio_dict = {}

    @property
    def pron(self):
        if self.word:
            data = {
                'text_to_transcribe': self.word,
                'submit': "Show+transcription",
                'output_dialect': 'br',
                'output_style': 'only_tr',
                'preBracket': '',
                'postBracket': '',
                'speech_support': '0'}

            response = requests.post('https://tophonetics.com/', data=data)

            for line in response.text.split('\n'):
                if line.startswith('<div id="transcr_output"><span class="transcribed_word">'):
                    word_plus = line[len('<div id="transcr_output"><span class="transcribed_word">'):]
                    pattern = r'^\w+'
                    match = re.match(pattern, word_plus)
                    if match:
                        pron = match.group(0)
                        logger.debug(f'Pron: {pron}')
                        return pron
        return ''

    def get_full_audio(self):
        url = f"https://d1qx7pbj0dvboc.cloudfront.net/{self.word}.mp3"
        params = {
            "headers": {
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0",
                "Accept": "audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5",
                "Accept-Language": "en-GB,en;q=0.5",
                "Range": "bytes=0-"
            },
        }
        response = requests.get(url, **params)
        file = response.content
        open(f'sounds/{self.word}.mp3', 'wb').write(file)
        self.full_audio_dict[self.word] = Audio(f'sounds/{self.word}.mp3')


    def get_phonemes(self):
        original_phonemes = list(self.pron)
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

    def set_positions(self):
        self.test_positions = {}
        for i in range(len(self.phonemes)):
            self.test_positions[i] = ''
        return self.test_positions

    def set_up_word(self, index):
        self.word = self.words.pop(index)
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
