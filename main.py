import json

from ursina import *

app = Ursina()

from phoneme_engine import PhonemeEngine
from game_scene import MainGame
from components import MyButtonList, MyInput

import logging

logger = logging.getLogger('pronBlocks')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
fh = logging.FileHandler('pronBlocks.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


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

        self.menu_help = Text("Use UP and DOWN arrows to navigate menu", parent=self.main_menu, y=-0.3, x=0,
                              origin=(0, 0), enabled=False)

        self.mbl = MyButtonList(button_dict={
            "Start": Func(self.start_game),
            "Words": Func(words_menu_btn),
            "Exit": Func(quit_game)
        }, y=-0.35, parent=self.main_menu)

        Text("OPTIONS MENU", parent=self.words_menu, y=0.4, x=0, origin=(0, 0))
        Text("Press ESC to go back, or Enter to update", parent=self.words_menu, y=-0.2, x=0, origin=(0, 0))

        def options_back_btn_action():
            self.main_menu.enable()
            self.words_menu.disable()

        Text("WORDS:", parent=self.words_menu, y=0.3, x=0, origin=(0, 0))
        Text.default_resolution = 16 * 2
        self.text_field = MyInput(self.update_word_list, parent=self.words_menu, y=0.2, enabled=False,
                                  wordwrap=64, max_lines=1)
        self.text_field.add_text(', '.join(self.word_list))

        Button("Back", parent=self.words_menu, y=-0.3, x=-0.3, scale=(0.1, 0.05), color=rgb(50, 50, 50),
               on_click=options_back_btn_action)
        Button("Update", parent=self.words_menu, y=-0.3, x=0.3, scale=(0.1, 0.05), color=rgb(50, 50, 50),
               on_click=self.update_word_list)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def start_game(self):
        self.update_word_list()
        word_list = self.word_list
        if self.game.phoneme_store is not None:
            if self.game.phoneme_store.words:
                self.game.phoneme_store.words.append(self.game.phoneme_store.word)
                word_list = self.game.phoneme_store.words
        logger.debug(f'Restarting game with: {word_list}')
        self.game.phoneme_store = PhonemeEngine(words=word_list)
        self.game_screen.enable()
        self.main_menu.disable()
        self.background.disable()
        self.game.build()
        self.game.player.enable()

    def update_word_list(self):
        self.word_list = re.split(' |, ', self.text_field.text)
        json_obj = {'word_list': self.word_list}
        with open('word_list.json', 'w') as f:
            json.dump(json_obj, f)
        logger.debug('Word list written to file')
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
                    self.game_screen.enable()
                    self.main_menu.disable()
                else:
                    application.quit()
            if key == "down":
                self.mbl.selection_marker.y -= 1
            if key == "up":
                self.mbl.selection_marker.y += 1

        if self.words_menu.enabled:
            if key == "escape":
                self.main_menu.enable()
                self.words_menu.disable()
                self.text_field.disable()

        if self.game_screen.enabled:
            if key == "escape":
                self.main_menu.enable()
                self.menu_help.enable()
                self.game.player.disable()
                self.game.reset_text.disable()
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

                    self.game.next_block.texture = PhonemeEngine.textures.get(self.game.phoneme_store.phonemes[-1],
                                                                              'index')
                else:
                    self.game.next_block.texture = 'index'

            if self.game.update_counter is not None:
                self.game.update_counter += 1
                if self.game.update_counter > 1000 and not self.game.correct:
                    self.game.give_up_button.enable()
                elif self.game.correct:
                    self.game.give_up_button.disable()


# Setup window title
window.title = "Pron Blocks"
window.fps_counter.disable()
window.fullscreen = True
window.exit_button.visible = False

# Call our menu
main_menu = MainScreen()

# Run application
app.run()
