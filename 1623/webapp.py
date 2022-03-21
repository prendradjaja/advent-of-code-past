from browser import document, html

import ast
import types

from virtual_machine import run
from util import strjoin, ints


# In js, i need to do Q = s => document.querySelector(s). I guess this is because Python binds methods at the dot, and JS binds at call time
Q = document.querySelector


class classes:  # css class names
    ACTIVE_HISTORY_TICK = 'active'


def main():
    global state, history

    state = types.SimpleNamespace()
    state.tick = 0

    instructions = [ints(l.rstrip('\n').split()) for l in open('in')]
    registers = {'a': 7, 'b': 0, 'c': 0, 'd': 0}
    history = run(instructions, registers, record_history=True)

    render_history()
    render_current_program_state()

    document.addEventListener('keydown', on_keydown)


def on_select_tick(tick):
    Q('.history').children[state.tick].classList.remove(classes.ACTIVE_HISTORY_TICK)
    state.tick = tick
    Q('.history').children[state.tick].classList.add(classes.ACTIVE_HISTORY_TICK)

    render_current_program_state()


def render_current_program_state():
    pstate = history[state.tick]
    Q('.registers').innerText = strjoin(pstate.registers.values(), '\t')

    instructions = ast.literal_eval(pstate.instructions_str)

    text = ''
    for i, line in enumerate(instructions + [['---']]):
        text += '* ' if i == pstate.ip else '  '
        text += f'{i:3}) {strjoin(line)}\n'
    Q('.code').innerText = text


def render_history():
    history_el = Q('.history')
    for i in range(len(history)):
        button_el = html.BUTTON(i)
        button_el.addEventListener('click',
            (lambda j:
                lambda event: on_select_tick(j)
            )(i)
        )
        history_el.appendChild(button_el)

    Q('.history button').classList.add(classes.ACTIVE_HISTORY_TICK)


def on_keydown(event):
    if event.key == 'ArrowLeft':
        new_tick = max(state.tick - 1, 0)
        on_select_tick(new_tick)
    elif event.key == 'ArrowRight':
        new_tick = min(state.tick + 1, len(history) - 1)
        on_select_tick(new_tick)
    elif event.key == 'ArrowUp':
        event.preventDefault()
        on_select_tick(0)
    elif event.key == 'ArrowDown':
        event.preventDefault()
        on_select_tick(len(history) - 1)


if __name__ == '__main__':
    main()
