from s import World, CLAY, SPRING, SPRING_POS, FLOWING_WATER, RESTING_WATER
from inputs import EXAMPLE_INPUT, REAL_INPUT


BOX_SIZE = 20
INPUT_TEXT = EXAMPLE_INPUT
STEPS = 50

BOX_SIZE = 5
INPUT_TEXT = REAL_INPUT
STEPS = 15000


PADDING = 5  # How many boxes of padding to display around the whole scene


CLASSES = {
    CLAY: 'clay',
    SPRING: 'spring',
    FLOWING_WATER: 'flowing-water',
    RESTING_WATER: 'resting-water',
}


def main():
    world = HTMLWorld.from_scan(INPUT_TEXT, SPRING_POS)
    for _ in range(STEPS):
        world.step()
    html = world.show_as_html()
    print(html)


class HTMLWorld(World):
    '''
    Like a World, but it can be rendered into static HTML.

    This could be all moved into the World class, but maybe it's nice to have
    everything browser-related in a separate place.
    '''

    def show_as_html(self):
        html = (
            '''
<html>
<head>
  <meta charset="utf-8">
  <style>
    .box {
      position: absolute;
'''.lstrip('\n') +
            f'''
      height: {BOX_SIZE}px;
      width: {BOX_SIZE}px;'''.strip('\n') +
            '''
    }
    .box.clay {
      background: black;
    }
    .box.spring {
      background: green;
    }
    .box.flowing-water {
      background: hotpink;
    }
    .box.resting-water {
      background: lightskyblue;
    }
  </style>
</head>
<body>'''.rstrip('\n')
        )

        min_x = min(x for (x, y) in self.clay)
        max_x = max(x for (x, y) in self.clay)
        min_y = min(y for (x, y) in self.clay)
        max_y = max(y for (x, y) in self.clay)

        for pos in self.clay:
            html += self.show_one_box(CLAY, pos, min_x, min_y)
        for pos in self.springs:
            html += self.show_one_box(SPRING, pos, min_x, min_y)
        for pos in self.flowing_water:
            html += self.show_one_box(FLOWING_WATER, pos, min_x, min_y)
        for pos in self.resting_water:
            html += self.show_one_box(RESTING_WATER, pos, min_x, min_y)

        html += '''
</body>
</html>
        '''.strip()
        return html

    def show_one_box(self, value, absolute_pos, min_x, min_y):
        html = ''
        ax, ay = absolute_pos

        # rx, ry = relative coordinates
        rx = ax - min_x + PADDING
        ry = ay - min_y + PADDING

        class_name = CLASSES[value]
        return (
            f'<div class="box {class_name}" style="' +
            f'left: {rx * BOX_SIZE}px; ' +
            f'top: {ry * BOX_SIZE}px"></div>'
        )


if __name__ == '__main__':
    main()
