import tkinter as tk
from tkinter.font import Font
import time
from threading import Thread

class MatrixText(tk.Label):
    """
    A derived class from the tk.Label class.
    This class is here to provide stylistic
    properties to the label, including the
    font which shows as an LED matrix style
    font.

    --------------
    custom methods
    --------------
        > scroll_text
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

    def scroll_text(self):
        """
        Function that creates the illusion of
        scrolling text by iterating through the
        characters in the text and removing, replacing
        the first and last characters.

        !! This function is blocking
        """
        destin_text = self['text'] + " "
        self.config(text = destin_text)
        self.update()
        self.update_idletasks()
        while True:
            for i in range(len(destin_text) + 1):
                self.config(text = destin_text[i:] + destin_text[:i])
                self.update()
                self.update_idletasks()
                time.sleep(0.5)
        

class DesktopTrainBoard(tk.Tk):
    '''
    A class that represents the overall
    application user interface, built of
    individual UI components as well
    as the functionality of updating the
    display.
    '''
    def __init__(self):
        super().__init__()
        self.title("Desktop Trainboard")
        self.geometry("300x150")
        self.resizable(width=False,height=False)
        self.attributes('-topmost', True)
        self.iconbitmap("assets/trainboard_icon.ico")
        #self.overrideredirect(True)
    
        self.ui_threads = []

        container = tk.Frame(self, bg="#000000")
        container.pack(expand=True, side="top", fill="both", anchor="w")

        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=1)
        container.grid_rowconfigure(2, weight=1)
        container.grid_columnconfigure(0, weight=0)
        container.grid_columnconfigure(1, weight=1)
        container.grid_columnconfigure(2, weight=0)

        message_container = tk.Frame(self, bg="#000000")
        message_container.pack(expand=True, side="top", fill="both", anchor="e")
    
        message_container.grid_rowconfigure(0, weight=1)
        message_container.grid_columnconfigure(0, weight=1)

        dispatch_rows = [
            DispatchRow(container, 0, ("1st", "London Kings Cross", "11:00")),
            DispatchRow(container, 1, ("2nd", "Exeter St Davids", "11:50")),
            DispatchRow(container, 2, ("3rd", "Bradford Forster Square", "12:00"))
        ]

        container.update_idletasks()
        container.update()

        for dispatch_row in dispatch_rows:
            destination_alloted_width = container.grid_bbox(column=1, row=dispatch_row.dispatch_row)[2]
            destination_actual_width = dispatch_row.final_destination.winfo_reqwidth()
            if (destination_actual_width > destination_alloted_width):
                pass
                #TODO Scroll logic here -- threading?
                

        MessageRow(message_container, "Some message...")


class DispatchRow:
    """
    A class that represents each single
    row of dispatch board, this includes
    the:
        - Ordinal position of the service (1st...3rd)
        - Final destination of the service (i.e. Birmingham)
        - Arrival or Departure time

    """
    def __init__(self, container: tk.Frame, row: int, dispatch_information: tuple):

        self.dispatch_row = row

        self.dispatch_ordinal = MatrixText(container)
        self.dispatch_ordinal.config(text=dispatch_information[0])

        self.final_destination = MatrixText(container)
        self.final_destination.config(text=dispatch_information[1])

        self.dispatch_time = MatrixText(container)
        self.dispatch_time.config(text=dispatch_information[2])
        
        self.dispatch_ordinal.grid(row=row, column=0, sticky="nsew", padx=(0,0))
        self.final_destination.grid(row=row, column=1, sticky="nsew", padx=(0,10))
        self.dispatch_time.grid(row=row, column=2, sticky="nsew")
    

class MessageRow(tk.Frame):
    def __init__(self, master, message_to_display: str):
        super().__init__(master, background="#000000")
        message = MatrixText(master)
        message.config(text=message_to_display)




if __name__ == "__main__":
    d = DesktopTrainBoard()

if __name__ == "__main__":
    app = DesktopTrainBoard()
    app.mainloop()