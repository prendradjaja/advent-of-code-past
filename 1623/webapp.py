from browser import document, html

import ast
import types

from virtual_machine import run
from util import strjoin, ints


S = lambda s: document.querySelector(s)

class classes:  # css class names
    ACTIVE_HISTORY_TICK = 'active'

def main():
    global state, history

    state = types.SimpleNamespace()
    state.tick = 0

    # text = ''
    # for line in open('ex'):
    #     text += line
    # S('.code').innerText = text

    instructions = [ints(l.rstrip('\n').split()) for l in open('in')]
    registers = {'a': 7, 'b': 0, 'c': 0, 'd': 0}
    history = run(instructions, registers, record_history=True)

    render_history()
    render_current_program_state()

    document.addEventListener('keydown', on_keydown)

    # print('--')
    # for each in history:
    #     print(each)


# ProgramState = namedtuple('ProgramState', 'instructions registers ip tick')


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


def on_select_tick(tick):
    S('.history').children[state.tick].classList.remove(classes.ACTIVE_HISTORY_TICK)
    state.tick = tick
    S('.history').children[state.tick].classList.add(classes.ACTIVE_HISTORY_TICK)

    render_current_program_state()


def render_current_program_state():
    pstate = history[state.tick]
    S('.registers').innerText = strjoin(pstate.registers.values(), '\t')

    instructions = ast.literal_eval(pstate.instructions_str)

    text = ''
    for i, line in enumerate(instructions + [['---']]):
        text += '* ' if i == pstate.ip else '  '
        text += f'{i:3}) {strjoin(line)}\n'
    S('.code').innerText = text


def render_history():
    history_el = S('.history')
    for i in range(len(history)):
        button_el = html.BUTTON(i)
        button_el.addEventListener('click',
            (lambda j:
                lambda event: on_select_tick(j)
            )(i)
        )
        history_el.appendChild(button_el)

    S('.history button').classList.add(classes.ACTIVE_HISTORY_TICK)



if __name__ == '__main__':
    main()
