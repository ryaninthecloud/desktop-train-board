from tkinter import Label
from tkinter.font import Font
from threading import Event, Thread
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

    def scroll_text(self, stop_event: Event) -> None:
        """
        Thread centric function that creates the illusion of
        scrolling text by iterating through the
        characters in the label text and removing, replacing
        the first and last characters.

        There are two sleep calls, within the iteration of
        text length is to make the text scrolling smooth,
        the second within the while True statement is
        to create a break between text scrolls

        :parameters:
            :stop_event: threading.Event to call to close the scroll safely 
        """
    
        text_to_scroll = self["text"] + " "
        self.config(text = text_to_scroll)
        self.update()
        self.update_idletasks()

        while True:
            if stop_event.isSet():
                break
            for i in range(len(text_to_scroll) + 1):
                self.config(text = text_to_scroll[i:] + text_to_scroll[:i])
                self.update()
                self.update_idletasks()
                time.sleep(0.4)

            time.sleep(1)

class ThreadSafetyContainer:
    """
    A class to wrap around any long-running
    threads used in the train board and the 
    associated event that can be used to signal
    a safe-stopping to the threaded function.
    """
    def __init__(self, thread: Thread, event: Event):
        """
        Initialisation of Thread Safety Container

        :parameters:
            thread: Thread: the thread that has been created
            event: Event: the event that has been passed to the threaded function
        """
        self.contained_thread = thread
        self.stoppage_event = event
    
    def safe_stop_thread(self) -> None:
        """
        A function to set the Event and then
        joining the thread for stopping.
        """

        self.stoppage_event.set()
        self.contained_thread.join()