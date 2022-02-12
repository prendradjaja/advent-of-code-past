from datetime import datetime


class ProgressBar:
    def __init__(self, total_steps, /, width=20):
        self.total_steps = total_steps
        self.width = width
        self.starttime = datetime.now()

    def show(self, current_step):
        now = datetime.now()
        filledwidth = int(current_step / self.total_steps * self.width)
        emptywidth = self.width - filledwidth
        bar = f'[{filledwidth * "="}{emptywidth * " "}]'

        timer = human_readable(now - self.starttime)

        # Warning: If a print is shorter than the previous print, it won't overwrite the whole thing
        print(
            '\r',
            bar + ' ',
            f'{current_step}/{self.total_steps} ',
            f'@ {timer}',

            end='',
            sep=''
        )


def human_readable(delta):
    raw = str(delta)
    timer = raw[:raw.index('.')+3] if '.' in raw else timer_raw


    if timer.startswith('0:00:'):
        return timer[5:].lstrip('0') + ' s'
    return timer
