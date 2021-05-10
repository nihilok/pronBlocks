import random
from random import randint
import requests
import re
from ursina import Audio

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
        'ɔ': 'o.png',
        'θ': 'th.png',
        'ʃ': 'sh.png',
        'ʧ': 'ch.png',
        'ɛ': 'e.png',
        'ʒ': 'zi.png',
        'e': 'e.png',
        'o': 'uh.png',
        'ɑ': 'o.png',
        'ɜ': 'ir.png',
        'ŋ': 'ng.png'
    }

    def __init__(self, words: list):
        self.phonemes = []
        self.original_phonemes = []
        self.words = words
        self.word = self.get_new_word()

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
                        return match.group(0)
        return self.pron()

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
        phonemes = original_phonemes.copy()
        random.shuffle(phonemes)
        return phonemes, original_phonemes

    def set_positions(self):
        self.test_positions = {}
        for i in range(len(self.phonemes)):
            self.test_positions[i] = ''
        return self.test_positions

    def get_new_word(self):
        if len(self.words) > 1:
            index = randint(0, len(self.words) - 1)
            self.word = self.words.pop(index)
            self.phonemes, self.original_phonemes = self.get_phonemes()
            self.set_positions()
        elif len(self.words) == 1:
            self.word = self.words.pop(0)
        else:
            self.word = None
        return self.word
