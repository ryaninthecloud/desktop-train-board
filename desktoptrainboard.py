import tkinter as tk
from auxiliary_components import MatrixText
import time
from threading import Thread
import requests

class DesktopTrainBoard(tk.Tk):
    """
    A class representing the train board application.
    A derived class of the the Tk class in Tkinter.
    """
    def __init__(self):
        super().__init__()
        """
        Initialisation of the application.

        :attributes:
            dispatch_container: tk.Frame containing dispatch rows
            message_container: tk.Frame containing service message row
            ui_threads: list of threads managing the updates to the gui
            dispatch_rows: list of DispatchRow objects within the dispatch_container 
        """
        self.title("Desktop Trainboard")
        self.geometry("300x150")
        self.resizable(width=False,height=False)
        self.attributes('-topmost', True)
        self.iconbitmap("assets/trainboard_icon.ico")

        self.dispatch_container = None
        self.message_container = None
        self.ui_threads = []
        self.dispatch_rows = []

        self.build_display_board()
    
        
        self.dispatch_rows = [
            DispatchRow(container = self.dispatch_container, row = 0),
            DispatchRow(container = self.dispatch_container, row = 1),
            DispatchRow(container = self.dispatch_container, row = 2)
        ]
    
    def build_display_board(self) -> None:
        """
        Builds the display board that will display
        the services.
        """
        self.dispatch_container = tk.Frame(self, bg="#000000")
        self.dispatch_container.pack(expand=True, side="top", fill="both", anchor="w")

        self.dispatch_container.grid_rowconfigure(0, weight=1)
        self.dispatch_container.grid_rowconfigure(1, weight=1)
        self.dispatch_container.grid_rowconfigure(2, weight=1)
        self.dispatch_container.grid_columnconfigure(0, weight=0)
        self.dispatch_container.grid_columnconfigure(1, weight=1)
        self.dispatch_container.grid_columnconfigure(2, weight=0)

        self.dispatch_container.update_idletasks()
        self.dispatch_container.update()

        self.message_container = tk.Frame(self, bg="#000000")
        self.message_container.pack(expand=True, side="top", fill="both", anchor="e")
    
        self.message_container.grid_rowconfigure(0, weight=1)
        self.message_container.grid_columnconfigure(0, weight=1)

        MessageRow(self.message_container, "Some message...")

    def get_train_services(self, endpoint: str = None) -> list[dict]:
        """
        Method that makes calls to the train services API
        to retrieve current services at a station.

        :parameters:
            endpoint: str: for future implementations to specify
                            the departure or arrival endpoint.
        
        :returns:
            train_services: list of dictionaries containing services
        """
        train_services = requests.request(
            method="get",
            url="put_in_variable"
        )
        train_services = train_services.json()
        return train_services["train_services"]

    def update_board(self):
        test_services = [
            {
                "ordinal":"1st",
                "destination":"VeryVeryVeryLong",
                "exp_time":"12:00"
            },
            {
                "ordinal":"2nd",
                "destination":"VeryVeryLong",
                "exp_time":"12:00"
            },
            {
                "ordinal":"3rd",
                "destination":"Long",
                "exp_time":"12:00"
            }
        ]

        for i, service in enumerate(test_services):
            self.dispatch_rows[i].set_row(service)

        for dispatch_row in self.dispatch_rows:
            destination_alloted_width = self.dispatch_container.grid_bbox(column=1, row=dispatch_row.dispatch_row)[2]
            destination_actual_width = dispatch_row.final_destination.winfo_reqwidth()
            if (destination_actual_width > destination_alloted_width):
                thread = Thread(target=dispatch_row.final_destination.scroll_text, daemon=True)
                self.ui_threads.append(thread)
                print(dispatch_row.final_destination['text'])
                thread.start()
    
    def main_application(self):
        while True:
            self.update_board()
            time.sleep(60)
    
    def start_board(self):
        thread = Thread(target=self.main_application, daemon=True)
        thread.start()


class DispatchRow:
    """
    A class that represents each single
    row of dispatch board, this includes
    the:
        - Ordinal position of the service (1st...3rd)
        - Final destination of the service (i.e. Birmingham)
        - Arrival or Departure time

    """
    def __init__(self, container: tk.Frame, row: int):

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
        self.dispatch_time.config(text=dispatch_information["exp_time"])


class MessageRow(tk.Frame):
    def __init__(self, master, message_to_display: str):
        super().__init__(master, background="#000000")
        message = MatrixText(master)
        message.config(text=message_to_display)

if __name__ == "__main__":
    app = DesktopTrainBoard()
    app.after(100, app.start_board)
    app.mainloop()