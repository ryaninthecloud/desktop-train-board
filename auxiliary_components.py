from tkinter import Label
from tkinter.font import Font
import time 

class MatrixText(Label):
    """
    A derived class from the tk.Label class.
    This class is here to provide stylistic
    properties to the label, including the
    font which shows as an LED matrix style
    font.

    :custom_methods:
        > scroll_text - scroll the label's current text
    """
    def __init__(self, master):
        matrix_font = Font(
            family="LED Counter 7",
            size="22"
        )
        super().__init__(master, 
                        font=matrix_font,
                        bg="#000000",
                        fg="#ffcc00",
                        justify="left",
                        anchor="nw")

    def scroll_text(self) -> None:
        """
        Blocking function that creates the illusion of
        scrolling text by iterating through the
        characters in the label text and removing, replacing
        the first and last characters.

        There are two sleep calls, within the iteration of
        text length is to make the text scrolling smooth,
        the second within the while True statement is
        to create a break between text scrolls
        """
    
        text_to_scroll = self["text"] + " "
        self.config(text = text_to_scroll)
        self.update()
        self.update_idletasks()

        while True:
            for i in range(len(text_to_scroll) + 1):
                self.config(text = text_to_scroll[i:] + text_to_scroll[:i])
                self.update()
                self.update_idletasks()
                time.sleep(0.4)

            time.sleep(1)