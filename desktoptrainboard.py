import tkinter as tk
from tkinter.font import Font

class MatrixText(tk.Label):
    """
    A derived class from the tk.Label class.
    This class contains only stylistic
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
            DispatchRow(container, 1, ("2nd", "Exeter", "11:50")),
            DispatchRow(container, 2, ("3rd", "Totnes", "12:00"))
        ]

        container.update_idletasks()
        container.update()

        for dispatch_row in dispatch_rows:
            destination_alloted_width = container.grid_bbox(column=1, row=dispatch_row.dispatch_row)[2]
            destination_actual_width = dispatch_row.final_destination.winfo_reqwidth()
            if (destination_actual_width > destination_alloted_width):
                pass
                #animate text

        MessageRow(message_container, "Some message...")

        self.mainloop()


class DispatchRow(tk.Frame):
    def __init__(self, container: tk.Frame, row: int, dispatch_information: tuple):
        super().__init__(master=container, bg="#000000")

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