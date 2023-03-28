# Made by Guillermo (William) Rubio on February 2023
import sys
import tkinter as tk
import webbrowser as wb

from tkinter import ttk
from tkinter import filedialog
import model_playground as mpl
from PIL import Image, ImageTk
import os
import datetime
import shutil

from ModelFactory import ModelFactory

DEFAULT_MODEL = str(os.path.abspath(os.path.join(os.getcwd(), os.pardir))) + "/models/es_dlm_03.h5"
single_directory = ""


def open_link(link):
    wb.open(link)


class MainFrame(tk.Tk):
    """
    Frame object referencing all pages of the GUI
    """

    def __init__(self):
        super().__init__()
        self.geometry("600x400")
        self.title("EquiScore")

        # Frames for each page
        self.home_frame = tk.Frame(self)
        self.function_frame = tk.Frame(self)
        self.generate_home_frame()
        self.generate_function_frame()
        self.show_home()

        self.destination_mul = None
        self.origin_mul = None
        self.classified = None
        self.default_model = str(os.path.abspath(os.path.join(os.getcwd(), os.pardir))) + "/models/es_dlm_03.h5"

    def add_data_new_model(self):
        data_dir = filedialog.askdirectory(
            initialdir=".",
            title="Select Data Directory",
        )
        my_model_factory = ModelFactory()
        my_model_factory.createModel(data_dir,  os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models')))


    def import_model(self):
        print("Current Model Directory = " + self.default_model)
        self.default_model = filedialog.askopenfilename(
            initialdir="../models",
            title="Select Image File",
            filetypes=[("HDF5 files", "*.h5")])
        print("New Model Directory = " + str(self.default_model))

    def multiple_run(self):
        if (self.destination_mul == None or self.origin_mul == None):
            print("Origen o destino no identificado")
            return -1

        # Create output Folder
        today = datetime.date.today().strftime('%d-%m-%Y')
        new_dir_name = f'Reconocimiento EquiScore del {today}'
        count = 1
        while os.path.exists(os.path.join(self.destination_mul, new_dir_name)):
            new_dir_name = f'Reconocimiento EquiScore del {today} - {count:02d}'
            count += 1

        os.makedirs(os.path.join(self.destination_mul, new_dir_name))

        for i in range(10):
            os.makedirs(os.path.join(self.destination_mul, new_dir_name, str(i)))

        os.makedirs(os.path.join(self.destination_mul, new_dir_name, "Not valid"))
        self.classified=os.path.join(self.destination_mul, new_dir_name)
        print("Created directory: " + self.classified)

        # Image iteration and clasification

        for file_name in os.listdir(self.origin_mul):
            # Check if the file is an image (e.g. a JPEG or PNG file)
            if file_name.endswith('.jpg') or file_name.endswith('.jpeg') or file_name.endswith('.png'):
                # If it is an image, process it and save it to the output directory
                image_path = os.path.join(self.origin_mul, file_name)
                self.process_image(image_path)
                print(f"Processed {image_path} and saved to {self.origin_mul}")



    def process_image(self, image_path):
        mp = mpl.ModelPlayground()
        h = mp.simple_prediction(self.default_model, image_path)
        if h == 10:
            h = "Not valid"
        shutil.copy(image_path, self.classified + "/" + str(h))



    def select_dir(self, des_orig, label):
        img_dir = filedialog.askdirectory(
            initialdir=".",
            title="Select Directory",
        )
        if des_orig == "destination":
            self.destination_mul = img_dir
            label.config(text="Output directory: " + str(self.destination_mul))
            label.pack()
        if des_orig == "origin":
            self.origin_mul = img_dir
            label.config(text="Input directory: " + str(self.origin_mul))
            label.pack()

        print(str(self.origin_mul) + "    " + str(self.destination_mul))

    def henneke_single_image(self, label):
        img_dir = filedialog.askopenfilename(
            initialdir=".",
            title="Select Image File",
            filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")))
        print("Img directory = " + img_dir)
        mp = mpl.ModelPlayground()

        h = mp.simple_prediction(self.default_model, img_dir)

        label.config(text="Henneke Score: " + str(h))
        label.pack()
        print(h)

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
                                   "is to accurately score horses body conditions using the Henneke Body Conditioning\n"
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

        tk.Button(sing_imag, text="Select Image", font="Roboto 20 ",
                  command=lambda: self.henneke_single_image(shown_score)).pack(pady=5)

        ttk.Separator(sing_imag, orient="horizontal").pack(fill="x", padx=10, pady=10)
        shown_score = tk.Label(sing_imag, text="No image selected", font=("Roboto", 16))
        shown_score.pack()

        # Multiple Image Frame
        tk.Label(mul_imag, text="Select a folder of images to process", font=("Roboto", 16)).pack(pady=10)
        tk.Button(mul_imag, text="Select Input Folder", font="Roboto 20",
                  command=lambda: self.select_dir("origin", input_tag)).pack(pady=10)
        input_tag = tk.Label(mul_imag, text="No input directory selected", font=("Roboto", 10))
        input_tag.pack()

        ttk.Separator(mul_imag, orient="horizontal").pack(fill="x", padx=10, pady=10)

        tk.Label(mul_imag, text="Select where you want your classified batch", font=("Roboto", 16)).pack(pady=10)
        tk.Button(mul_imag, text="Select Output Folder", font="Roboto 20",
                  command=lambda: self.select_dir("destination", output_tag)).pack(pady=10)
        output_tag = tk.Label(mul_imag, text="No output directory selected", font=("Roboto", 10))
        output_tag.pack()

        ttk.Separator(mul_imag, orient="horizontal").pack(fill="x", padx=10, pady=10)

        tk.Button(mul_imag, text="Run", font="Roboto 30 bold", command=self.multiple_run).pack(pady=10)

        # Advanced Frame
        tk.Label(advanced, text="Create new model with new data (please be patient)", font=("Roboto", 16)).pack(pady=10)
        tk.Button(advanced, text="Add", font="Roboto 20", command=self.add_data_new_model).pack(pady=5)
        ttk.Separator(advanced, orient="horizontal").pack(fill="x", padx=10, pady=10)
        tk.Label(advanced, text="Import model to use by default", font=("Roboto", 16)).pack(pady=10)
        tk.Button(advanced, text="Import", font="Roboto 20",command=self.import_model).pack(pady=5)
        ttk.Separator(advanced, orient="horizontal").pack(fill="x", padx=10, pady=10)
        tk.Label(advanced, bd=0, relief="solid", font=("Roboto", 14), justify=tk.LEFT,
                              text="Warning: this tab is used to create new models, adding new data using the output \n"
                                   "directory format. To update your default model, use import model. The global de- \n"
                                   "fault model for EquiScore will be updated by the author, as it learns to score \n"
                                   "horses with better accuracy.").pack(pady=10)


MainFrame().mainloop()
