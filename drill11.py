from pico2d import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def draw_boy(boy):
    flip = 'h' if boy.direction < 0 else ''
    boy.image.clip_composite_draw(
        boy.frame * 100, 0, 100, 100,
        0, flip,
        boy.x, boy.y, boy.size, boy.size
    )


class Idle:
    @staticmethod
    def enter(boy, event):
        boy.frame = 0

    @staticmethod
    def exit(boy, event):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        draw_boy(boy)


class Run:
    @staticmethod
    def enter(boy, event):
        boy.frame = 0
        boy.direction = -1 if event == 'LEFT' else 1

    @staticmethod
    def exit(boy, event):
        pass

    @staticmethod
    def do(boy):
        boy.x += boy.direction * 3
        boy.frame = (boy.frame + 1) % 8
        half_size = boy.size / 2
        boy.x = max(half_size, min(SCREEN_WIDTH - half_size, boy.x))

    @staticmethod
    def draw(boy):
        draw_boy(boy)


class Boy:
    def __init__(self):
        self.image = load_image('run_animation.png')
        self.x = SCREEN_WIDTH // 2
        self.y = 90
        self.frame = 0
        self.direction = 1
        self.size = 70
        self.state = None
        self.change_state(Idle, None)

    def change_state(self, new_state, event):
        if self.state is not None:
            self.state.exit(self, event)
        self.state = new_state
        self.state.enter(self, event)

    def handle_event(self, event):
        if event.type != SDL_KEYDOWN:
            return

        if self.state == Idle:
            if event.key == SDLK_LEFT:
                self.change_state(Run, 'LEFT')
            elif event.key == SDLK_RIGHT:
                self.change_state(Run, 'RIGHT')
        elif self.state == Run:
            if event.key == SDLK_LEFT:
                self.direction = -1
            elif event.key == SDLK_RIGHT:
                self.direction = 1

    def update(self):
        self.state.do(self)

    def draw(self):
        self.state.draw(self)


def main():
    open_canvas(SCREEN_WIDTH, SCREEN_HEIGHT)
    grass = load_image('grass.png')
    boy = Boy()
    running = True

    while running:
        clear_canvas()
        grass.draw(SCREEN_WIDTH // 2, 30)
        boy.update()
        boy.draw()
        update_canvas()

        for event in get_events():
            if event.type == SDL_QUIT:
                running = False
            elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                running = False
            else:
                boy.handle_event(event)

        delay(0.05)

    close_canvas()


if __name__ == '__main__':
    main()
