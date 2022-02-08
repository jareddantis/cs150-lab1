from toga import Label
from toga.style import Pack
from .constants import COLOR_GREEN, COLOR_GREY

class WordleLetter(Label):
    def __init__(self, letter: str):
        super().__init__(letter, style=Pack(
            flex=1,
            text_align='center',
            color=COLOR_GREY
        ))

        self._green = False
        self._visible = True
    
    @property
    def visible(self) -> bool:
        return self._visible
    
    @visible.setter
    def visible(self, value: bool):
        self._visible = value
        if value:
            self.style.update(visibility='visible')
        else:
            self.style.update(visibility='hidden')
    
    @property
    def green(self) -> bool:
        return self._green
    
    @green.setter
    def green(self, value: bool):
        self._green = value
        if value:
            self.style.update(font_weight='bold', color=COLOR_GREEN)
        else:
            self.style.update(font_weight='normal', color=COLOR_GREY)
    
    def reset(self):
        """
        Resets the letter to its initial state.
        """
        self.green = False
        self.visible = True
        self.enabled = True
