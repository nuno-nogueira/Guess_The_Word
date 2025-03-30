from tkinter import *
from tkinter import ttk
from game_settings_screen import ClassicModeSettings
from game_settings_screen import FlagModeSettings
from PIL import Image, ImageTk
import os

class GamemodeScreenApp:
    def __init__(self, window):
        self.window = window
        self.setup_gamemode_screen()
    
    def setup_gamemode_screen(self):
        """
        Contains all widgets in the Gamemode Screen!
        """
        #---> Frames
        self.classic_mode_frame = Frame(self.window, width= 470, height=550, bg="lightgrey")
        self.classic_mode_frame.place(x = 20, y = 70)

        self.flag_mode_frame = Frame(self.window, width=470, height=550, bg="lightgrey")
        self.flag_mode_frame.place(x = 510, y = 70)
        
        #---> Gamemode Icons
        img_path = os.path.join("images","classic_mode_icon.png")
        img = Image.open(img_path)
        img = img.resize((128, 128))
        open_new_img = ImageTk.PhotoImage(img)
        self.classic_mode_icon = Label(self.classic_mode_frame, image = open_new_img, bg = "lightgrey")
        self.classic_mode_icon.image = open_new_img
        self.classic_mode_icon.place(x = 170, y = 70)

        img_path = os.path.join("images","flag_mode_icon.png")
        img = Image.open(img_path)
        img = img.resize((128, 128))
        open_new_img = ImageTk.PhotoImage(img)
        self.flag_mode_icon = Label(self.flag_mode_frame, image = open_new_img, bg = "lightgrey")
        self.flag_mode_icon.image = open_new_img
        self.flag_mode_icon.place(x = 170, y = 70)


        #---> Gamemode descriptions
        self.classic_mode_description = Label(self.classic_mode_frame, bg="lightgrey", text="-> A classic experience! Guess the word by \ndiscovering its letters and their positions!\nChoose from a variety of categories!", font=("Arial", 16)).place(x = 20, y = 300)
        
        self.flag_mode_description = Label(self.flag_mode_frame, bg="lightgrey", text="-> A new addition! Guess the country by \nits flag! (All classic rules still apply!)\nChoose from a variety of continents!", font=("Arial", 16)).place(x = 40, y = 300)

        # Gamemode buttons
        self.play_classic_mode = Button(self.classic_mode_frame, text="Play!", width=14, height=2, border=2, font=("Helvetica", 14), command=lambda:self.classic_mode())
        self.play_classic_mode.place(x = 150, y = 420)

        self.play_flag_mode = Button(self.flag_mode_frame, text="Play!", width=14, height=2, border=2, font=("Helvetica", 14), command=lambda: self.flag_mode())
        self.play_flag_mode.place(x = 150, y = 420)


    def classic_mode(self):
        """
        This function will remove all the Gamemode Screen's widgets
        and setup all widgets from the Classic Mode window!
        """
        self.classic_mode_frame.place_forget()
        self.flag_mode_frame.place_forget()

        ClassicModeSettings(self.window)


    def flag_mode(self):
        """
        This function will remove all the Gamemode Screen's widgets
        and setup all widgets from the Flag Mode window!
        """
        self.classic_mode_frame.place_forget()
        self.flag_mode_frame.place_forget()

        FlagModeSettings(self.window)