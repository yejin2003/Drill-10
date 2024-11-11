# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, load_font
from state_machine import *
from ball import Ball
import game_world
import game_framework

PIXEL_PER_METER=(10.0/0.3)
RUN_SPEED_KMPH=20.0
RUN_SPEED_MPM=(RUN_SPEED_KMPH*1000.0/60.0)
RUN_SPEED_MPS=(RUN_SPEED_MPM/60.0)
RUN_SPEED_PPS=(RUN_SPEED_MPS*PIXEL_PER_METER)

TIME_PER_ACTION=0.25
ACTION_PER_TIME=1.0/TIME_PER_ACTION
FRAMES_PER_ACTION=14

class Idle:
    @staticmethod
    def enter(boy, e):
        if start_event(e):
            boy.action = 3
            boy.face_dir = 1
        elif right_down(e) or left_up(e):
            boy.action = 2
            boy.face_dir = -1
        elif left_down(e) or right_up(e):
            boy.action = 3
            boy.face_dir = 1

        boy.frame = 0
        boy.wait_time = get_time()

    @staticmethod
    def exit(boy, e):
        if space_down(e):
            boy.fire_ball()

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION* ACTION_PER_TIME * game_framework.frame_time) % 8
        if get_time() - boy.wait_time > 2:
            boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        if boy.face_dir==-1:
            boy.image.clip_composite_draw(int(boy.frame) * 183, boy.action * 338, 183, 168, 0, 'h', boy.x+25, boy.y-25,100,100)
        else:
            boy.image.clip_composite_draw(int(boy.frame) * 183, boy.action * 338, 183, 168, 0, ' ', boy.x + 25,
                                          boy.y - 25, 100, 100)


class Sleep:
    @staticmethod
    def enter(boy, e):
        if start_event(e):
            boy.face_dir = 1
            boy.action = 3
        boy.frame = 0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8


    @staticmethod
    def draw(boy):
        if boy.face_dir == -1:
            boy.image.clip_composite_draw(int(boy.frame) * 183, boy.action * 338, 183, 168, 0, 'h', boy.x + 25,
                                          boy.y - 25, 100, 100)
        else:
            boy.image.clip_composite_draw(int(boy.frame) * 183, boy.action * 338, 183, 168, 0, ' ', boy.x + 25,
                                          boy.y - 25, 100, 100)


class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            boy.dir, boy.face_dir, boy.action = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            boy.dir, boy.face_dir, boy.action = -1, -1, 0

    @staticmethod
    def exit(boy, e):
        if space_down(e):
            boy.fire_ball()


    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        boy.x += boy.dir * RUN_SPEED_PPS * game_framework.frame_time


    @staticmethod
    def draw(boy):
        if boy.face_dir == -1:
            boy.image.clip_composite_draw(int(boy.frame) * 183, boy.action * 338, 183, 168, 0, 'h', boy.x + 25,
                                          boy.y - 25, 100, 100)
        else:
            boy.image.clip_composite_draw(int(boy.frame) * 183, boy.action * 338, 183, 168, 0, ' ', boy.x + 25,
                                          boy.y - 25, 100, 100)





class Boy:

    def __init__(self,x,y):
        self.x, self.y = x,y
        self.frame=0
        self.action=3
        self.face_dir = 1
        self.dir=1
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, time_out: Sleep, space_down: Idle},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Run},
                Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle}
            }
        )
        self.font=load_font('ENCR10B.TTF',16)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        if (self.x > 1500): self.dir = -1
        if (self.x < 100): self.dir = 1
        pass

    def handle_event(self, event):
        pass

    def draw(self):
        action = 0
        if (self.frame < 5): action = 2
        if (self.frame > 4 and self.frame < 10): action = 1
        if (self.frame > 14):
            self.frame = 0
            action = 2

        if self.dir == -1:
            self.image.clip_composite_draw(int(self.frame % 5) * 183, 168 * action, 183, 168,
                                           0, 'h', self.x + 25, self.y - 25, 100, 100)
        else:
            self.image.clip_composite_draw(int(self.frame % 5) * 183, 168 * action, 183, 168,
                                           0, '', self.x - 25, self.y - 25, 100, 100)