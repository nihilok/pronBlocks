import json

from ursina import *

app = Ursina()
ARENA_DEPTH = 7


from phoneme_engine import PhonemeEngine
from game_scene import MainGame


class WordInputScreen(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui, ignore_paused=True)
        self.theme_music = Audio('sounds/Digital.mp3', autoplay=True, volume=0.1, loop=True)

        # Create empty entities that will be parents of our menus content
        self.main_menu = Entity(parent=self, enabled=True)
        self.options_menu = Entity(parent=self, enabled=False)
        self.main_game = MainGame(enabled=False, parent=self)
        with open('word_list.json', 'r') as f:
            self.word_list = json.load(f)['word_list']

        # [MAIN MENU] WINDOW START
        self.background = Sprite('index', color=color.dark_gray, z=1, scale=3)

        # Main Title:
        Text("PRON BLOCKS", parent=self.main_menu, y=0.4, x=0, origin=(0, 0))

        # Reference of our action function for quit button
        def quit_game():
            application.quit()

        # Reference of our action function for options button
        def options_menu_btn():
            self.options_menu.enable()
            self.main_menu.disable()

        def start_game():
            self.main_game.phoneme_store = PhonemeEngine(self.word_list)
            self.main_game.build()
            self.main_game.enable()
            self.main_menu.disable()
            self.background.disable()
            self.main_game.generate_player()

        # Button list
        ButtonList(button_dict={
            "Start": Func(start_game),
            "Words": Func(options_menu_btn),
            "Exit": Func(quit_game)
        }, y=-0.3, parent=self.main_menu)
        # [MAIN MENU] WINDOW END

        # [OPTIONS MENU] WINDOW START
        # Title of our menu
        Text("OPTIONS MENU", parent=self.options_menu, y=0.4, x=0, origin=(0, 0))

        # Reference of our action function for back button
        def options_back_btn_action():
            self.main_menu.enable()
            self.options_menu.disable()

        def update_word_list():
            # self.word_list = [word.strip() for word in self.text_field.text.split()]
            self.word_list = re.split(' |, ', self.text_field.text)
            json_obj = {'word_list': self.word_list}
            with open('word_list.json', 'w') as f:
                json.dump(json_obj, f)
            self.main_menu.enable()
            self.options_menu.disable()

        Text("WORDS:", parent=self.options_menu, y=0.3, x=0, origin=(0, 0))
        Text.default_resolution = 16 * 2
        self.text_field = TextField(parent=self.options_menu, y=0.2, enabled=True,
                                    wordwrap=64)
        self.text_field.add_text(', '.join(self.word_list))

        # Buttons
        Button("Back", parent=self.options_menu, y=-0.3, x=-0.3, scale=(0.1, 0.05), color=rgb(50, 50, 50),
               on_click=options_back_btn_action)
        Button("Update", parent=self.options_menu, y=-0.3, x=0.3, scale=(0.1, 0.05), color=rgb(50, 50, 50),
               on_click=update_word_list)
        # [OPTIONS MENU] WINDOW END

        for key, value in kwargs.items():
            setattr(self, key, value)

    def input(self, key):

        if self.main_menu.enabled:
            if key == "escape":
                # Close app
                application.quit()

        if self.options_menu.enabled:
            if key == "escape":
                # Close options window and show main menu
                self.main_menu.enable()
                self.options_menu.disable()

        if self.main_game.enabled:
            if key == "escape":
                # Close help window and show main menu
                application.quit()

    def update(self):
        self.main_game.spin_block()

# Setup window title
window.title = "Pron Blocks"
window.fps_counter.disable()
window.fullscreen = True
window.exit_button.visible = False

# Call our menu
main_menu = WordInputScreen()

# Run application
app.run()