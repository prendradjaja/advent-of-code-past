# See ./with-external-script-file.html

from browser import document, html

from s import World, CLAY, SPRING, SPRING_POS, FLOWING_WATER, RESTING_WATER
from inputs import EXAMPLE_INPUT, REAL_INPUT


BOX_SIZE = 20
INPUT_TEXT = EXAMPLE_INPUT

BOX_SIZE = 3
INPUT_TEXT = REAL_INPUT


PADDING = 5  # How many boxes of padding to display around the whole scene


CLASSES = {
    CLAY: 'clay',
    SPRING: 'spring',
    FLOWING_WATER: 'flowing-water',
    RESTING_WATER: 'resting-water',
}


def main():
    world = BrowserWorld.from_scan(INPUT_TEXT, SPRING_POS)
    for _ in range(50):
        world.step()
    world.show_in_browser()


class BrowserWorld(World):
    '''
    Like a World, but it can be rendered in the browser.

    This could be all moved into the World class, but maybe it's nice to have
    everything browser-related in a separate place.
    '''

    def show_in_browser(self):
        min_x = min(x for (x, y) in self.contents)
        max_x = max(x for (x, y) in self.contents)
        min_y = min(y for (x, y) in self.contents)
        max_y = max(y for (x, y) in self.contents)

        # ax, ay = absolute coordinates
        for ay in range(min_y - PADDING, max_y + PADDING + 1):
            for ax in range(min_x - PADDING, max_x + PADDING + 1):
                pos = (ax, ay)
                if pos in self.contents:
                    self.show_one_box(pos, min_x, min_y)

    def show_one_box(self, absolute_pos, min_x, min_y):
        ax, ay = absolute_pos

        # rx, ry = relative coordinates
        rx = ax - min_x + PADDING
        ry = ay - min_y + PADDING

        box = html.DIV()
        document <= box
        box.classList.add('box')
        box.classList.add(CLASSES[self.contents[absolute_pos]])
        box.style.left   = f'{rx * BOX_SIZE}px'
        box.style.top    = f'{ry * BOX_SIZE}px'
        box.style.height = f'{BOX_SIZE}px'
        box.style.width  = f'{BOX_SIZE}px'


if __name__ == '__main__':
    main()
