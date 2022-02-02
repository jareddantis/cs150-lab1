from toga import Box, Label
from toga.style import Pack
from toga.style.pack import ROW
from typing import List
from .words import STATE_CORRECT, STATE_MISPLACED

class GuessRow(Box):
    def __init__(self):
        super().__init__(style=Pack(
            flex=1,
            direction=ROW,
            padding=10
        ))

        # Create five boxes and store them for later
        self.boxes = []
        for _ in range(5):
            box = Box(style=Pack(
                width=50,
                height=45,
                padding=2,
                background_color='grey',
                alignment='center'
            ))
            self.add(box)
            self.boxes.append(box)

    def update(self, letters: List[str], states: List[bool]):
        for i, letter in enumerate(letters):
            label = Label(letter.upper(), style=Pack(
                flex=1,
                height=40,
                padding_top=7,
                font_size=16,
                font_weight='bold',
                text_align='center',
            ))
            if states[i] == STATE_CORRECT:
                # Letter is correct, turn box green
                self.boxes[i].style.update(background_color='#00a323')
            elif states[i] == STATE_MISPLACED:
                # Letter is misplaced, turn box yellow
                self.boxes[i].style.update(background_color='#b88700')
            self.boxes[i].add(label)
