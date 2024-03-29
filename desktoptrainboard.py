import tkinter as tk
from auxiliary_components import MatrixText, ThreadSafetyContainer, DispatchRow, MessageRow
import time
from threading import Thread, Event
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
            ui_threads: list of tuples for threads and events managing the updates to the gui
            dispatch_rows: list of DispatchRow objects within the dispatch_container 
        """
        self.title("Desktop Trainboard")
        self.geometry("300x200")
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

        self.message_row = MessageRow(self.message_container, "Connecting...")
    
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

        self.message_container = tk.Frame(self, bg="#ffffff")
        self.message_container.pack(expand=True, side="top", fill="both", anchor="w")
    
        self.message_container.grid_rowconfigure(0, weight=1)
        self.message_container.grid_columnconfigure(0, weight=1)

        

        self.message_container.update_idletasks()
        self.message_container.update()

    def get_service_data(self, endpoint: str = None) -> list[dict]:
        """
        Method that makes calls to the train services API
        to retrieve current services at a station.

        :parameters:
            endpoint: str: for future implementations to specify
                            the departure or arrival endpoint.
        
        :returns:
            service_data: dictionary response
        """
        try:
            service_data = requests.request(
                method="get",
                url="var"
            )
        except:
            self.message_row.update_message("Error cx to API...")
            return False
        service_data = service_data.json()
        return service_data

    def safe_stop_ui_threads(self):
        """
        Safely stop any running UI threads by setting their
        event and then waiting for the thread to join.
        """
        if self.ui_threads:
            for thread_safety_container in self.ui_threads:
                thread_safety_container.safe_stop_thread()

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
        print("**BOARD UPDATE STARTING**")
        
        service_data = self.get_service_data()

        while not service_data:
            time.sleep(1)
            print("retrying cx")
            self.message_row.update_message("Retrying...")
            time.sleep(2)
            self.get_service_data()
        
        print("stopping thread")
        self.safe_stop_ui_threads()
        self.ui_threads.clear()

        for i, service in enumerate(service_data["train_services"]):
            print("train services updated", service['destination'])
            self.dispatch_rows[i].set_row(service)

        self.message_row.message.config(text=service_data["warning_messages"])
        message_scroll_stop_event = Event()
        message_scroll_thread = Thread(target=self.message_row.message.scroll_text, daemon=True, args=(message_scroll_stop_event,))
        message_thread_safety_container = ThreadSafetyContainer(thread = message_scroll_thread, event = message_scroll_stop_event)
        self.ui_threads.append(message_thread_safety_container)
    
        for dispatch_row in self.dispatch_rows:
            print("evaluating row")
            destination_alloted_width = self.dispatch_container.grid_bbox(column=1, row=dispatch_row.dispatch_row)[2]
            destination_actual_width = dispatch_row.final_destination.winfo_reqwidth()
            if (destination_actual_width > destination_alloted_width):
                print("longer than display destination")
                stop_event = Event()
                thread = Thread(target=dispatch_row.final_destination.scroll_text, args=(stop_event,), daemon=True)
                thread_safety_container = ThreadSafetyContainer(thread = thread, event = stop_event)
                self.ui_threads.append(thread_safety_container)
                print("thread managed for", dispatch_row.final_destination['text'])
        
        if self.ui_threads:
            [thread.contained_thread.start() for thread in self.ui_threads]
    
    def main_application(self):
        while True:
            self.update_board()
            time.sleep(1)
    
    def start_board(self):
        thread = Thread(target=self.main_application, daemon=True)
        thread.start()

if __name__ == "__main__":
    app = DesktopTrainBoard()
    app.after(100, app.start_board)
    app.mainloop()