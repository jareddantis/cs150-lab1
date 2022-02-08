from toga import Label
from toga.style import Pack
from .constants import COLOR_GREEN, COLOR_GREY

class WordleLetter(Label):
    def __init__(self, letter: str):
        super().__init__(letter, style=Pack(
            flex=1,
            text_align='center'
        ))

        self._green = False
    
    @property
    def green(self):
        return self._green
    
    @green.setter
    def green(self, value: bool):
        self._green = value
        if value:
            self.style.update(font_weight='bold', color=COLOR_GREEN)
        else:
            self.style.update(font_weight='normal', color=COLOR_GREY)
