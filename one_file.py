import json
import random
import requests
import re
import logging
from random import randint
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from typing import Optional

app = Ursina()
ARENA_DEPTH = 7
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
app_id = 'cc2a92a7'
app_key = '0ed75d7d62b9eabd0231cbaadef1f995'

language = 'en-gb'
# fields = 'registers,domainClasses,pronunciations'
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
        'ɡ': Audio('sounds/g.mp3', autoplay=False),
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
        'aɪ': Audio('sounds/ai.mp3', autoplay=False),
        'eə': Audio('sounds/euh.mp3', autoplay=False),
        'əʊ': Audio('sounds/oh.mp3', autoplay=False),
        'ʊə': Audio('sounds/uuh.mp3', autoplay=False),
        'ɪə': Audio('sounds/iuh.mp3', autoplay=False),
        'aʊ': Audio('sounds/au.mp3', autoplay=False),
        'ɔɪ': Audio('sounds/oy.mp3', autoplay=False),
        'eɪ': Audio('sounds/ei.mp3', autoplay=False),
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
        'ɡ': 'textures/g.png',
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
        'aɪ': 'textures/ai.png',
        'ɑ': 'textures/ar.png',
        'ʌ': 'textures/uhh.png',
        'eə': 'textures/euh.png',
        'əʊ': 'textures/oh.png',
        'ʊə': 'textures/uuh.png',
        'ɪə': 'textures/iuh.png',
        'aʊ': 'textures/au.png',
        'ɔɪ': 'textures/oy.png',
        'eɪ': 'ei.png'
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
            return self.pron_response[0][0]
        else:
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
        return None

    def get_full_audio(self):
        if self.pron_response:
            url = self.pron_response[1]
            response = requests.get(url)
        else:
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
        pron = self.pron()
        print(pron)
        if pron:
            pron = pron.replace('əː', 'ɜː')
            pron = pron.replace('a', 'æ')
            pron = pron.replace('ɛː', 'eə')
            pron = pron.replace('ɛ', 'e')
            pron = pron.replace('ʌɪ', 'aɪ')
            pron = pron.replace('(ə)', '')
            pron = pron.replace('tʃ', 'ʧ')
            original_phonemes = list(pron)
            if "'" in original_phonemes:
                original_phonemes.remove("'")
            if "," in original_phonemes:
                original_phonemes.remove(",")
            if 'ˈ' in original_phonemes:
                original_phonemes.remove('ˈ')
            if 'ˌ' in original_phonemes:
                original_phonemes.remove('ˌ')
            colons = 0
            for i in range(len(original_phonemes)-1):
                if original_phonemes[i] == 'ː':
                    colons += 1
            for i in range(colons):
                original_phonemes.remove('ː')
            diphthongs = {'aɪ', 'eə', 'əʊ', 'ʊə', 'ɪə', 'aʊ', 'ɔɪ', 'eɪ'}
            phonemes = []
            subs = [pron[i: j] for i in range(len(pron)) for j in range(i + 1, len(pron) + 1) if
                   len(pron[i:j]) == 2]
            for sub in subs:
                if sub in diphthongs:
                    for i, p in enumerate(original_phonemes):
                        if i < len(original_phonemes):
                            if p == sub[0] and original_phonemes[i+1] == sub[1]:
                                original_phonemes[i] = sub
                                original_phonemes.pop(i+1)



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




class Voxel(Button):
    def __init__(self, engine: PhonemeEngine, parent_game, position=(0, 0, 0), texture='rect835.png',
                 text: Optional[str] = '', **kwargs):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(.9, 1.0)),
            text=text,
            text_color=color.red,
            double_sided=True,
            **kwargs
        )
        self.phoneme_store = engine
        self.parent_game = parent_game

    def play_sound(self, text):
        sound = PhonemeEngine.sounds.get(text)
        if sound is not None:
            sound.play()

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                if not self.parent_game.started:
                    self.parent_game.started = True
                if len(self.phoneme_store.phonemes):
                    if self.position[2] == ARENA_DEPTH:
                        if not self.text:
                            phoneme = self.phoneme_store.phonemes.pop(-1)
                            print(phoneme)
                            voxel = Voxel(self.phoneme_store, self.parent_game, position=self.position + mouse.normal,
                                          texture=self.phoneme_store.textures.get(phoneme, 'white_cube'), text=phoneme, highlight_color=color.white)
                            self.parent_game.voxels.append(voxel)
                            self.parent_game.score -= 1
                            self.phoneme_store.test_positions.append((self.position[0], phoneme))
                            self.play_sound(phoneme)
                            logger.debug(phoneme)
                            if not len(self.phoneme_store.phonemes):
                                invoke(self.check_win, delay=.5)
                        else:
                            self.play_sound(self.text)

                else:
                    self.play_sound(self.text)

            if key == 'right mouse down':
                if self.text:
                    if not self.parent_game.correct:
                        self.phoneme_store.phonemes.append(self.text)
                        self.parent_game.voxels.remove(self)
                        if (self.position[0], self.text) in self.phoneme_store.test_positions:
                            self.phoneme_store.test_positions.remove((self.position[0], self.text))
                        destroy(self)
                    else:
                        self.play_sound(self.text)

    def check_win(self):
        check = ''.join([p[1] for p in list(sorted(self.phoneme_store.test_positions))])
        test = ''.join(self.phoneme_store.original_phonemes)
        if check == test and not self.parent_game.correct:
            self.parent_game.help_text.text = 'CORRECT!'
            PhonemeEngine.sounds.get('win').play()
            self.parent_game.correct = True
            self.parent_game.score += len(self.phoneme_store.original_phonemes) + self.parent_game.difficulty
            invoke(self.phoneme_store.full_audio_dict[self.phoneme_store.word].play, delay=1)
            invoke(self.parent_game.build, delay=4)
        elif not self.parent_game.correct and check != test:
            logger.debug(check + ' ' + test)
            print(check + ' ' + test)
            PhonemeEngine.sounds.get('lose').play()


class MainGame(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.phoneme_store = None
        self.voxels = []
        self.correct = False
        self.started = False
        self.update_counter = None
        self.score = 0
        self.difficulty = 3     # lower difficulty is harder
        self.help_text = Text(
            '',
            parent=camera.ui,
            x=-.6,
            y=.35,
            enabled=False
        )
        self.score_text = Text(
            '',
            parent=camera.ui,
            x=.5,
            y=.35,
            enabled=False
        )
        self.player = None
        self.ground = Entity(model='plane', scale=(100, 1, 100), y=-1, color=color.yellow.tint(-.2), texture='white_cube',
                             texture_scale=(100, 100), collider='box', enabled=False)
        self.sky = Entity(model='sphere', texture='sky2.jpg', scale=10000, double_sided=True, color=color.white, enabled=False)
        self.rotated_y = 30
        self.next_block = Entity(parent=camera.ui, rotation=Vec3(10, 30, 30), model='cube', scale=.1, x=.7, y=.2, texture='index')
        self.give_up_button = Button(parent=scene, text='give up', double_sided=True, x=-1, z=ARENA_DEPTH, y=3, on_click=self.give_up, enabled=False, scale_x=2)
        self.reset_text = Text(
            'Press ESC to change words and/or start again.',
            parent=scene,
            x=0, z=ARENA_DEPTH, y=2,
            double_sided=True,
            enabled=False,
            scale=15
        )

    def create_clouds(self):
        self.sky.enable()
        for i in range(20):
            cloud = Entity(parent=scene, model='cube', texture='index', scale_x=random.randint(2, ARENA_DEPTH), scale_y=random.randint(1, 6), scale_z=random.randint(2, ARENA_DEPTH), color=color.white, position=Vec3(random.randint(-50, ARENA_DEPTH+50), random.randint(10, 50), random.randint(-50, ARENA_DEPTH+50)))
            self.voxels.append(cloud)

    def give_up(self):
        self.score -= 1
        if self.phoneme_store.words:
            self.build()
        else:
            self.end_game()

    def end_game(self):
        self.destroy_all()
        self.build_platform()
        self.correct = False
        self.update_counter = None
        self.update_score()
        if self.score > 0:
            self.help_text.text = f'GAME OVER! YOU WIN!\nYour score: {self.score}'
        else:
            self.help_text.text = f'GAME OVER! YOU LOSE!\nYour score: {self.score}'

    def reset(self):
        pass

    def build(self):
        self.started = True
        word = self.phoneme_store.get_new_word()
        self.update_counter = 0
        if self.give_up_button.enabled:
            self.give_up_button.disable()
        if self.reset_text.enabled:
            self.reset_text.disable()
        if self.ground.enabled:
            self.ground.disable()
        if word is not None:
            if self.phoneme_store.pron() is not None:
                self.help_text.text = f'The word is: "{self.phoneme_store.word}"\nLeft click in the green area to lay a phoneme,\nright click to pick one up.'
                self.help_text.enable()
                self.score_text.text = f'Score: {self.score}'
                self.score_text.enable()
                if self.voxels:
                    self.destroy_all()
                    self.help_text.text = self.phoneme_store.word
                    self.correct = False
                for z in range(ARENA_DEPTH + 1):
                    voxel_side_wall = Voxel(self.phoneme_store, self, position=(-1, 1, z))
                    voxel_other_side_wall = Voxel(self.phoneme_store, self, position=(len(self.phoneme_store.phonemes), 1, z))
                    self.voxels.append(voxel_side_wall)
                    self.voxels.append(voxel_other_side_wall)
                    for x in range(len(self.phoneme_store.phonemes)):
                        voxel = Voxel(self.phoneme_store, self, position=(x, 0, z))
                        voxel_wall = Voxel(self.phoneme_store, self, position=(x, 1, -1))
                        self.voxels.append(voxel)
                        self.voxels.append(voxel_wall)
                        if voxel.position[2] == ARENA_DEPTH:
                            voxel.color = color.lime
                            voxel.texture = 'white_cube'
                invoke(self.create_clouds, delay=0.1)
                if self.player:
                    self.player.y = 0
                    self.player.x = len(self.phoneme_store.phonemes) // 2
                    self.player.z = 1
                else:
                    self.generate_player()
            else:
                return self.build()
        else:
            self.end_game()


    def build_platform(self):

        self.ground.enable()
        self.update_counter = None
        self.reset_text.enable()
        self.give_up_button.disable()
        self.create_clouds()
        self.started = False

    def update_score(self):
        self.score_text.text = f'Score: {self.score}'

    def destroy_all(self):
        for v in self.voxels:
            destroy(v)
        self.voxels = []

    def generate_player(self):
        self.player = FirstPersonController(enabled=True)
        self.player.speed += 2
        self.player.mouse_sensitivity = Vec2(50, 50)
        self.player.jump_duration = .3
        self.player.gravity *= .8
        self.player.y = 0
        self.player.x = len(self.phoneme_store.phonemes) // 2
        self.player.z = 1

    def spin_block(self):
        self.rotated_y -= 1
        self.next_block.rotation = Vec3(10, self.rotated_y, 30)


class MyInput(TextField):
    def __init__(self, update_func, **kwargs):
        super().__init__(**kwargs)
        self.update_func = update_func

    def input(self, key):
        super().input(key)


class MyButtonList(ButtonList):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.action = None

    def input(self, key):
        super().input(key)
        if key == 'down arrow':
            y = round(abs(self.highlight.y / self.button_height))
            if y < len(self.actions) - 1:
                if not self.selection_marker.enabled:
                    self.selection_marker.enable()
                else:
                    self.highlight.y -= self.button_height
                self.selection_marker.y = self.highlight.y
                y = round(abs(self.highlight.y / self.button_height))
            self.action = self.actions[y]

        if key == 'up arrow':
            y = round(abs(self.highlight.y / self.button_height))
            if y > 0:
                if not self.selection_marker.enabled:
                    self.selection_marker.enable()
                else:
                    self.highlight.y += self.button_height
                self.selection_marker.y = self.highlight.y
                y = round(abs(self.highlight.y / self.button_height))
            self.action = self.actions[y]

class MainScreen(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui, ignore_paused=True)
        self.theme_music = Audio('sounds/Digital.mp3', autoplay=True, volume=0.1, loop=True)
        self.main_menu = Entity(parent=self, enabled=True)
        self.words_menu = Entity(parent=self, enabled=False)
        self.game_screen = Entity(parent=self, enabled=False)
        self.game = MainGame(parent=self.game_screen, enabled=False)
        self.background = Sprite('index', parent=camera.ui, color=color.dark_gray, z=1, scale=1)
        try:
            with open('word_list.json', 'r') as f:
                self.word_list = json.load(f)['word_list']
        except:
            self.word_list = ['word', 'example', 'amazing']

        Text("PRON BLOCKS", parent=self.main_menu, y=0.4, x=0, origin=(0, 0), scale=3)

        def quit_game():
            application.quit()

        def words_menu_btn():
            self.words_menu.enable()
            self.main_menu.disable()
            self.text_field.enable()

        self.mbl = MyButtonList(button_dict={
            "Start": Func(self.start_game),
            "Words": Func(words_menu_btn),
            "Exit": Func(quit_game)
        }, y=-0.35, parent=self.main_menu)

        Text("OPTIONS MENU", parent=self.words_menu, y=0.4, x=0, origin=(0, 0))

        def options_back_btn_action():
            self.main_menu.enable()
            self.words_menu.disable()

        Text("WORDS:", parent=self.words_menu, y=0.3, x=0, origin=(0, 0))
        Text.default_resolution = 16 * 2
        self.text_field = MyInput(self.update_word_list, parent=self.words_menu, y=0.2, enabled=False,
                                  wordwrap=64, max_lines=1)
        self.text_field.add_text(', '.join(self.word_list))

        # Buttons
        Button("Back", parent=self.words_menu, y=-0.3, x=-0.3, scale=(0.1, 0.05), color=rgb(50, 50, 50),
               on_click=options_back_btn_action)
        Button("Update", parent=self.words_menu, y=-0.3, x=0.3, scale=(0.1, 0.05), color=rgb(50, 50, 50),
               on_click=self.update_word_list)
        # [OPTIONS MENU] WINDOW END

        for key, value in kwargs.items():
            setattr(self, key, value)

    def start_game(self):
        self.game.phoneme_store = PhonemeEngine(words=self.word_list)
        self.game_screen.enable()
        self.main_menu.disable()
        self.background.disable()
        self.game.build()

    def update_word_list(self):
        self.word_list = re.split(' |, ', self.text_field.text)
        json_obj = {'word_list': self.word_list}
        with open('word_list.json', 'w') as f:
            json.dump(json_obj, f)
        self.main_menu.enable()
        self.words_menu.disable()
        self.text_field.disable()

    def input(self, key):
        if key == 'enter':
            if self.main_menu.enabled and self.mbl.action:
                if callable(self.mbl.action):
                    self.mbl.action()
                elif isinstance(self.mbl.action, Sequence):
                    self.mbl.action.start()
            elif self.words_menu.enabled:
                self.update_word_list()

        if self.main_menu.enabled:
            if key == "escape":
                if self.game.started:
                    # Resume
                    self.game_screen.enable()
                    self.main_menu.disable()
                else:
                    # Close the app
                    application.quit()
            if key == "down":
                self.mbl.selection_marker.y -= 1
            if key == "up":
                self.mbl.selection_marker.y += 1

        if self.words_menu.enabled:
            if key == "escape":
                # Close options window and show main menu
                self.main_menu.enable()
                self.words_menu.disable()
                self.text_field.disable()

        if self.game_screen.enabled:
            if key == "escape":
                # Close help window and show main menu
                self.main_menu.enable()
                self.game_screen.disable()

    def update(self):
        self.game.spin_block()
        if self.game.started:
            if self.game.player.y <= -100:
                self.game.player.y = 0
                self.game.score -= 1
            self.game.update_score()
            if self.game.phoneme_store:
                if self.game.phoneme_store.phonemes:
               
                    self.game.next_block.texture = PhonemeEngine.textures.get(self.game.phoneme_store.phonemes[-1], 'index')
                else:
                    self.game.next_block.texture = 'index'

            if self.game.update_counter is not None:
                self.game.update_counter += 1
                if self.game.update_counter > 1000:
                    self.game.give_up_button.enable()

# Setup window title
window.title = "Pron Blocks"
window.fps_counter.disable()
window.fullscreen = True
window.exit_button.visible = False

# Call our menu
main_menu = MainScreen()

# Run application
app.run()
