from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

from voxel import Voxel
from constants import ARENA_DEPTH


class MainGame(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.phoneme_store = None
        self.voxels = []
        self.correct = False
        self.started = False
        self.score = -1
        self.help_text = Text(
            '',
            parent=self,
            x=-.5,
            y=.4,
            enabled=False
        )
        self.score_text = Text(
            '',
            parent=self,
            x=.5,
            y=.4,
            enabled=False
        )
        self.player = None

    def build(self):
        self.score += 1
        word = self.phoneme_store.get_new_word()
        print(word)
        print(self.phoneme_store.phonemes)
        if word is not None:
            while not self.phoneme_store.phonemes:
                time.sleep(0.2)
            self.help_text.text = f'The word is: "{self.phoneme_store.word}"\nLeft click in the green area to lay a phoneme,\nright click to pick one up.'
            self.help_text.enable()
            self.score_text.text = f'Score: {self.score}'
            self.score_text.enable()
            if self.voxels:
                for v in self.voxels:
                    destroy(v)
                self.voxels = []
                # display_text_input()
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
            if self.player:
                self.player.y = 0
                self.player.x = len(self.phoneme_store.phonemes) // 2
                self.player.z = 1
        else:
            print_on_screen(f'GAME OVER! YOU WIN!\nYour score: {self.score}')

    def generate_player(self):
        self.player = FirstPersonController()
        self.player.y = 0
        self.player.x = len(self.phoneme_store.phonemes) // 2
        self.player.z = 1

    def update(self):
        if self.player.y <= -100:
            self.player.y = 0
            self.score -= 1