from typing import Optional

from ursina import *
from constants import ARENA_DEPTH
from phoneme_engine import PhonemeEngine


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
                            voxel = Voxel(self.phoneme_store, self.parent_game, position=self.position + mouse.normal,
                                          texture=self.phoneme_store.textures.get(phoneme, 'white_cube'), text=phoneme, highlight_color=color.gray)
                            self.parent_game.voxels.append(voxel)
                            self.phoneme_store.test_positions[self.position[0]] = phoneme
                            self.play_sound(phoneme)
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
                        self.phoneme_store.test_positions[self.position[0]] = ''
                        destroy(self)
                    else:
                        self.play_sound(self.text)

    def check_win(self):
        check = ''.join(self.phoneme_store.test_positions.values())
        test = ''.join(self.phoneme_store.original_phonemes)
        print(check)
        print(test)
        if check == test and not self.parent_game.correct:
            self.parent_game.help_text.text = 'CORRECT!'
            PhonemeEngine.sounds.get('win').play()
            self.parent_game.correct = True
            invoke(self.parent_game.build, delay=2)
        elif not self.parent_game.correct and check != test:
            PhonemeEngine.sounds.get('lose').play()
