# Made by Guillermo (William) Rubio on February 2023
import tkinter as tk
import webbrowser as wb
from tkinter import ttk


def open_link(link):
    wb.open(link)


class MainFrame(tk.Tk):
    """
    Frame object referencing all pages of the GUI
    """

    def __init__(self):
        super().__init__()
        self.geometry("600x400")
        self.title("EquiScore - Home")

        # Frames for each page
        self.home_frame = tk.Frame(self)
        self.function_frame = tk.Frame(self)
        self.generate_home_frame()
        self.generate_function_frame()
        self.show_home()

    def show_home(self):
        # Show the home page
        self.home_frame.pack(fill=tk.BOTH, expand=True)
        self.function_frame.pack_forget()

    def show_funtion(self):
        # Show the function page
        self.function_frame.pack(fill=tk.BOTH, expand=True)
        self.home_frame.pack_forget()

    def generate_home_frame(self):
        # Home page
        tk.Label(self.home_frame, text="EquiScore", font="Roboto 60 bold").pack(padx=10, pady=10)
        tk.Label(self.home_frame, text="An open source project made by William Rubio", font=("Roboto", 20)).pack()
        # Internet buttons
        buttonframe = tk.Frame(self.home_frame)
        buttonframe.columnconfigure(0, weight=1)
        buttonframe.columnconfigure(1, weight=1)
        btn1 = tk.Button(buttonframe, text="GitHub", font=("Roboto", 18),
                         command=lambda: open_link("https://github.com/guillerubio/EquiScore"))
        btn1.grid(row=0, column=0, sticky=tk.W + tk.E)
        btn2 = tk.Button(buttonframe, text="Project Website", font=("Roboto", 18),
                         command=lambda: open_link("https://www.william-rubio.com/bcs-ai"))
        btn2.grid(row=0, column=2, sticky=tk.W + tk.E)
        buttonframe.pack(padx=10, pady=10)
        # Description and start
        descriptor = tk.Label(self.home_frame, bd=0, relief="solid", font=("Roboto", 14), justify=tk.LEFT,
                              text="EquiScore is convulational neural network AI made with Tensorflow. It's objective \n"
                                   "is to accurately score horses body conditions Using The Henneke Body Conditioning\n"
                                   "Scoring System. Start scoring your horses today!"
                              )
        descriptor.pack(padx=20, pady=20)
        tk.Button(self.home_frame, text="Get Started!", font="Roboto 30 bold",
                  command=self.show_funtion).pack(pady=40)

    def generate_function_frame(self):
        # Create the notebook
        notebook = ttk.Notebook(self.function_frame)
        notebook.pack(fill="both", expand=True)

        # Create the frames for each tab
        sing_imag = tk.Frame(notebook)
        mul_imag = tk.Frame(notebook)
        advanced = tk.Frame(notebook)

        # Add the frames to the notebook
        notebook.add(sing_imag, text="Single image")
        notebook.add(mul_imag, text="Multiple Images")
        notebook.add(advanced, text="Advanced")

        # Single Image Frame
        tk.Label(sing_imag, text="Select an image to body condition score", font=("Roboto", 16)).pack(pady=10)
        tk.Button(sing_imag, text="Select Image", font="Roboto 20 bold").pack(pady=5)

        # Multiple Image Frame
        tk.Label(mul_imag, text="Select a folder of images to process", font=("Roboto", 16)).pack(pady=10)
        tk.Button(mul_imag, text="Select Input Folder", font="Roboto 20 bold").pack(pady=0)
        ttk.Separator(mul_imag, orient="horizontal").pack(fill="x", padx=10, pady=30)
        tk.Label(mul_imag, text="Select where you want your classified batch", font=("Roboto", 16)).pack(pady=10)
        tk.Button(mul_imag, text="Select Output Folder", font="Roboto 20 bold").pack(pady=0)
        # Advanced Frame
        tk.Label(advanced, text="Create model on new data", font=("Roboto", 16)).pack(pady=10)
        tk.Button(advanced, text="Create", font="Roboto 20 bold").pack(pady=5)
        tk.Label(advanced, text="Add data to existing model", font=("Roboto", 16)).pack(pady=10)
        tk.Button(advanced, text="Add", font="Roboto 20 bold").pack(pady=5)
        tk.Label(advanced, text="Import model", font=("Roboto", 16)).pack(pady=10)
        tk.Button(advanced, text="Import", font="Roboto 20 bold").pack(pady=5)




MainFrame().mainloop()
