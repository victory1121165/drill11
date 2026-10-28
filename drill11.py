from pico2d import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def draw_boy(boy):
    boy.image.clip_draw(
        boy.frame * 100, 0, 100, 100,
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


class Boy:
    def __init__(self):
        self.image = load_image('run_animation.png')
        self.x = SCREEN_WIDTH // 2
        self.y = 90
        self.frame = 0
        self.direction = 1
        self.size = 70
        self.state = Idle
        self.state.enter(self, None)

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

        delay(0.05)

    close_canvas()


if __name__ == '__main__':
    main()
