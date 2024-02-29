from tkinter import Label, Frame
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
            for i in range(len(text_to_scroll) + 1):
                self.config(text = text_to_scroll[i:] + text_to_scroll[:i])
                self.update()
                self.update_idletasks()
                time.sleep(0.4)
            if stop_event.isSet():
                print("!!!!event stoppage")
                break
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

class DispatchRow:
    """
    A class that represents each single
    row of dispatch board, this includes
    the:
        - Ordinal position of the service (1st...3rd)
        - Final destination of the service (i.e. Birmingham)
        - Arrival or Departure time

    """
    def __init__(self, container: Frame, row: int):

        self.dispatch_row = row
        self.dispatch_ordinal = MatrixText(container)
        self.final_destination = MatrixText(container)
        self.dispatch_time = MatrixText(container)

        self.dispatch_ordinal.grid(row=row, column=0, sticky="nsew", padx=(0,0))
        self.final_destination.grid(row=row, column=1, sticky="nsew", padx=(0,10))
        self.dispatch_time.grid(row=row, column=2, sticky="nsew")
    
    def set_row(self, dispatch_information: dict) -> None:
        """
        Updates or inserts the dispatch row information:
            - ordinal
            - final destination
            - exp/sch arrival time
        
        :parameters
            dipatch_information: dictionary: should have the following keys
                - ordinal
                - destination
                - exp_time
                - sch_time
        """
        self.dispatch_ordinal.config(text=dispatch_information["ordinal"])
        self.final_destination.config(text=dispatch_information["destination"])

        if dispatch_information["exp_time"] == "On time":
            self.dispatch_time.config(text=dispatch_information["sch_time"], fg="#4CBB17")
        
        else:
            self.dispatch_time.config(text=dispatch_information["exp_time"], fg="#EE4B2B")


class MessageRow(Frame):
    def __init__(self, container: Frame, message_to_display: str):
        super().__init__(container, background="#000000")
        self.message = MatrixText(container)
        self.message.grid(row=0, column=0, sticky="nsew", padx=(0,0))
        self.message.config(text=message_to_display)
    
    def update_message(self, new_message: str):
        """
        A method to update the message within
        the row.
        """
        self.message.config(text=new_message)
