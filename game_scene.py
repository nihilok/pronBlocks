import random

from ursina import Entity, Text, camera, Vec3, application, color, destroy, Button, scene, invoke, Vec2
from ursina.prefabs.first_person_controller import FirstPersonController

from phoneme_engine import PhonemeEngine
from voxel import Voxel
from constants import ARENA_DEPTH


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

    # def update(self):
    #     print('working')
    #     if self.player.y <= -100:
    #         self.player.y = 0
    #         self.score -= 1
    #     self.update_score()
    #     if self.phoneme_store:
    #         print('Phoneme store:')
    #         if self.phoneme_store.phonemes:
    #             print(self.phoneme_store.phonemes)
    #             self.next_block.texture = PhonemeEngine.textures[self.phoneme_store.phonemes[-1]]
    #     else:
    #         self.next_block.texture = 'index'
    #     self.spin_block()
    #     if self.update_counter is not None:
    #         self.update_counter += 1
    #         if self.update_counter > 1000:
    #             self.give_up_button.enable()
