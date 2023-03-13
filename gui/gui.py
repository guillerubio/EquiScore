# Made by Guillermo (William) Rubio on February 2023
import tkinter as tk
import webbrowser as wb


# tk.set_appearance_mode("system")
# tk.set_default_color_theme("dark-blue")

def open_link(link):
    wb.open(link)



class MainFrame:
    """
    Frame object referencing all pages of the GUI
    """
    def __init__(self):
        self.running_page=self.WelcomePage().root
        self.running_page.mainloop()

    def mod_running_page(self, new_page):
        self.running_page.destroy()
        self.running_page = new_page
        self.running_page.mainloop()


    class WelcomePage:
        # Home
        def __init__(self):
            # Title and internet buttons
            self.root = tk.Tk()
            self.root.geometry("600x400")
            self.root.title("EquiScore - Home")

            self.label = tk.Label(self.root, text="EquiScore", font="Roboto 60 bold")
            self.label.pack(padx=10, pady=10)
            self.label = tk.Label(self.root, text="An open source project made by William Rubio", font=("Roboto", 20))
            self.label.pack()

            self.buttonframe = tk.Frame(self.root)
            self.buttonframe.columnconfigure(0, weight=1)
            self.buttonframe.columnconfigure(1, weight=1)

            self.btn1 = tk.Button(self.buttonframe, text="GitHub", font=("Roboto", 18),
                                  command=lambda: open_link("https://github.com/guillerubio/EquiScore"))
            self.btn1.grid(row=0, column=0, sticky=tk.W + tk.E)

            self.btn2 = tk.Button(self.buttonframe, text="Project Website", font=("Roboto", 18),
                                  command=lambda: open_link("https://www.william-rubio.com/bcs-ai"))
            self.btn2.grid(row=0, column=2, sticky=tk.W + tk.E)

            self.buttonframe.pack(padx=10, pady=10)

            # Description and start

            self.label3 = tk.Label(self.root, bd=0, relief="solid", font=("Roboto", 14), justify=tk.LEFT,
                                   text="EquiScore is convulational neural network AI made with Tensorflow. It's objective \n"
                                        "is to accurately score horses body conditions Using The Henneke Body Conditioning\n"
                                        "Scoring System. Start scoring your horses today!"
                                   )
            self.label3.pack(padx=20, pady=20)

            self.button3 = tk.Button(self.root, text="Get Started!", font="Roboto 30 bold", command=self.root.destroy)
            self.button3.pack(pady=40)



    class NumberPicPage:
        print("hello")



MainFrame()
