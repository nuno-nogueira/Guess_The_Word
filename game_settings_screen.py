from tkinter import *
from tkinter import messagebox
from game import Game
from PIL import Image, ImageTk
import os


# Classic Mode
class ClassicModeSettings:
    def __init__(self, window):
        self.window = window
        self.difficulty_selected = ""
        self.category_selected = ""
        self.hints = 0

        self.load_user_info()
        self.word_bank_progression()
        self.setup_game_settings_screen()


    def setup_game_settings_screen(self):
        """
        This function has all the game setting's widgets!
        """
        #----> Frames
        self.category_frame = Frame(self.window, width=450, height=400, bg="lightgrey")
        self.category_frame.place(x = 30, y = 60)

        self.difficulty_frame = Frame(self.window, width=450, height=400, bg="lightgrey")
        self.difficulty_frame.place(x = 520, y = 60)

        self.word_bank_frame = Frame(self.window, width=950, height=250, bg="lightgrey")
        self.word_bank_frame.place(x = 25, y = 520)

        self.play_button = Button(self.window, text="Play!",bg="lightgrey", width=10, height=1, border=2, font=("Helvetica", 18, "bold"), command=lambda:self.start_game())
        self.play_button.place(x = 425, y = 465)

        #--> Go back button
        icon_path = os.path.join("images","go_back_icon.png")
        icon = Image.open(icon_path)
        icon = icon.resize((44, 44))
        open_new_icon = ImageTk.PhotoImage(icon)
        self.go_back_button = Button(self.window, image=open_new_icon, bg="lightgrey", command = lambda: self.go_back())
        self.go_back_button.image = open_new_icon
        self.go_back_button.place(x = 920, y = 5)

        #----> Category Frame Widgets
        self.category_title = Label(self.category_frame, text="Categories", bg="lightgrey", font=("Arial", 18, "bold")).place(x = 160, y = 10)

        self.animal_category = Button(self.category_frame, text="Animals", width=9, height=1, border=2, bg="lightgrey", font=("Helvetica", 16), command=lambda:self.change_category("Animals"))
        self.job_category = Button(self.category_frame, text="Jobs", width=9, height=1, border=2, bg="lightgrey", font=("Helvetica", 16), command=lambda:self.change_category("Jobs"))
        self.colors_category = Button(self.category_frame, text="Colors", width=9, height=1, border=2, bg="lightgrey", font=("Helvetica", 16), command=lambda:self.change_category("Colors"))
        self.fruits_category = Button(self.category_frame, text="Fruits", width=9, height=1, border=2, bg="lightgrey", font=("Helvetica", 16), command=lambda:self.change_category("Fruits"))

        self.animal_category.place(x = 70, y = 100)
        self.job_category.place(x = 270, y = 100)
        self.colors_category.place(x = 70, y = 200)
        self.fruits_category.place(x = 270, y = 200)

        self.show_category = StringVar()
        self.show_category.set("Category selected -> {}".format(self.category_selected))
        self.show_category_lbl = Label(self.category_frame, bg="lightgrey", textvariable=self.show_category, font=("Arial", 16))
        self.show_category_lbl.place( x= 80, y = 310)

        #----> Difficulty Frame widgets
        self.difficulty_title = Label(self.difficulty_frame, text="Difficulties", bg="lightgrey", font=("Arial", 18, "bold"))
        self.difficulty_title.place(x = 160, y = 10)

        self.easy_difficulty = Button(self.difficulty_frame, text="Easy", width=9, height=1, border=2, bg="#84f069", fg="white", font=("Helvetica", 16, "bold"), command=lambda:self.change_difficulty("Easy"))
        self.medium_difficulty = Button(self.difficulty_frame, text="Medium", width=9, height=1, border=2, bg="#e0e342", fg="white", font=("Helvetica", 16, "bold"), command=lambda:self.change_difficulty("Medium"))
        self.hard_difficulty = Button(self.difficulty_frame, text="Hard", width=9, height=1, border=2, bg="#de1c07", fg="white", font=("Helvetica", 16, "bold"), command=lambda:self.change_difficulty("Hard"))
        self.challenge_difficulty = Button(self.difficulty_frame, text="Challenge", width=9, height=1, border=2, bg="#751207", fg="white", font=("Helvetica", 16, "bold"), command=lambda:self.change_difficulty("Challenge"))
        self.random_difficulty = Button(self.difficulty_frame, text="Random", width=9, height=1, border=2, bg="white", fg="black", font=("Helvetica", 16, "bold"), command=lambda:self.change_difficulty("Random"))

        self.easy_difficulty.place(x = 70, y = 60)
        self.medium_difficulty.place(x = 270, y = 60)
        self.hard_difficulty.place(x = 70, y = 160)
        self.challenge_difficulty.place(x = 270, y = 160)
        self.random_difficulty.place(x = 175, y = 240)

        self.show_difficulty = StringVar()
        self.show_difficulty.set("Difficulty selected -> {}".format(self.difficulty_selected))
        self.show_difficulty_lbl = Label(self.difficulty_frame, bg="lightgrey", textvariable=self.show_difficulty, font=("Arial", 16))
        self.show_difficulty_lbl.place( x= 75, y = 310)


        icon_path = os.path.join("images","tutorial_icon.png")
        icon = Image.open(icon_path)
        icon = icon.resize((44, 44))
        open_new_icon = ImageTk.PhotoImage(icon)
        self.tutorial_icon = Button(self.difficulty_frame, image=open_new_icon, bg="white", command = lambda: self.difficulty_explanation())
        self.tutorial_icon.image = open_new_icon
        self.tutorial_icon.place(x = 395, y = 5)

        #---> Word Bank Progression Frame Widgets
        self.word_bank_frame_title = Label(self.word_bank_frame, text = "Word Bank Progression", font=("Arial", 22,"bold"), bg="lightgrey").place(x = 280, y = 10)

        self.total_words_lbl = Label(self.word_bank_frame, text="Total Words \nfound:\n{}/{}".format(self.total_words_found, self.total_words), font=("Arial", 18, "bold"), bg="lightgrey").place(x = 375, y = 62)

        self.easy_words_lbl1 = Label(self.word_bank_frame, text="Easy", font=("Arial", 18, "bold"), fg="white", bg="#84f069")
        self.easy_words_lbl2 = Label(self.word_bank_frame, text="words found:\n{}/{}" .format(self.easy_words_found, self.easy_words), bg="lightgrey", font=("Arial", 16))

        self.easy_words_lbl1.place(x = 40, y = 70)
        self.easy_words_lbl2.place(x = 10, y = 105)

        self.medium_words_lbl1 = Label(self.word_bank_frame, text="Medium", font=("Arial", 18, "bold"), fg = "white", bg="#e0e342")
        self.medium_words_lbl2 = Label(self.word_bank_frame, text="words found:\n{}/{}" .format(self.medium_words_found, self.medium_words), bg="lightgrey", font=("Arial", 16))

        self.medium_words_lbl1.place(x = 190, y = 70)
        self.medium_words_lbl2.place(x = 180, y = 105)

        self.hard_words_lbl1 = Label(self.word_bank_frame, text="Hard", font=("Arial", 18, "bold"), fg="white", bg="#de1c07")
        self.hard_words_lbl2 = Label(self.word_bank_frame, text="words found:\n{}/{}" .format(self.hard_words_found, self.hard_words), bg="lightgrey", font=("Arial", 16))
        
        self.hard_words_lbl1.place(x = 620, y = 70)
        self.hard_words_lbl2.place(x = 590, y = 105)

        self.challenge_lbl1 = Label(self.word_bank_frame, text="Challenges", font=("Arial", 18, "bold"), fg="white", bg="#751207")
        self.challenge_lbl2 = Label(self.word_bank_frame, text="complete:\n{}/{}".format(self.challenges_complete, self.challenges_available), bg="lightgrey", font=("Arial", 16))

        self.challenge_lbl1.place(x = 770, y = 70)
        self.challenge_lbl2.place(x = 790, y = 105)

        self.reset_word_bank_btn = Button(self.word_bank_frame, text="Reset Word Bank", font=("Arial", 14), border=2 , width=15, height=1, command=lambda: self.reset_word_bank())
        self.reset_word_bank_btn.place(x = 750, y = 10)



    #---> Word Bank Functions
    
    def word_bank_progression(self):
        """
        This function has several functionalities which mostly tells the user their progression on the game
        It mostly counts the total words the user found and how many words there are still to find for each
        category
        """
        self.words_list = []
        self.total_words = 0
        self.total_words_found = 0
        self.easy_words = 0
        self.easy_words_found = 0
        self.medium_words = 0
        self.medium_words_found = 0
        self.hard_words = 0
        self.hard_words_found = 0
        self.challenges_complete = 0
        self.challenges_available = 0

        base_dir = os.path.dirname(os.path.abspath(__file__))
        list_of_files = ["animals.txt","fruits.txt","colors.txt","jobs.txt"]
        self.challenges_available = len(list_of_files)

        #--> Add all the words to the "self.words_list" array
        for file in list_of_files:
            file_path = os.path.join(base_dir, "Word Bank", file)

            with open(file_path, "r", encoding="utf-8") as f:
                words = f.readlines()

            for word in words:
                if "Challenge complete" in word:
                    if word == "Challenge complete? Yes":
                        self.challenges_complete += 1
                else:
                    self.words_list.append(word)

        self.total_words = len(self.words_list)

        word_length = 0
        #--> Count all the words found by the user!
        for word in self.words_list:
            if ";" in word:
                word_length = len(word[0:word.find(";") - 1])
            else:
                word_length = len(word)
            if ";guessed" in word:
                self.total_words_found += 1
            if word_length <= 5:
                self.easy_words += 1
                if ";guessed" in word:
                    self.easy_words_found += 1
            if word_length >= 6 and word_length <= 9:
                self.medium_words += 1
                if ";guessed" in word:
                    self.medium_words_found += 1
            if word_length >= 10:
                self.hard_words += 1
                if ";guessed" in word:
                    self.hard_words_found += 1      
            

    def reset_word_bank(self):
        """
        This function will let the user reset the "Word Bank"
        By doing so, all words that were previously found will be reset and can be picked again
        to be guessed again
        This basically resets all the progression the user made
        """

        answer = messagebox.askquestion("Reset Word Bank", 
        "Are you sure? If so, all the progression you've made will be reset and all the words you found can be selected again for you to guess!")


        if answer == "yes":
            self.words_list = []

            base_dir = os.path.dirname(os.path.abspath(__file__))
            list_of_files = ["animals.txt","fruits.txt","colors.txt","jobs.txt"]
            change_files = [] #This array will store the last word of each file so when the word bank is being updated, the words will go to their respective files

            #--> Add all the words to the "self.words_list" array
            for file in list_of_files:
                file_path = os.path.join(base_dir, "Word Bank", file)

                with open(file_path, "r", encoding="utf-8") as f:
                    words = f.readlines()

                if "Challenge complete? No" in words:
                    words.remove("Challenge complete? No")
                elif "Challenge complete? Yes" in words:
                    words.remove("Challenge complete? Yes")

                for i in range (len(words)):
                    if ";guessed" in words[i]:
                        words[i] = words[i][0:words[i].find(";")]
                        words[i] = words[i] + "\n"
                    if words[i] == words[len(words) - 1]:
                            change_files.append(words[i])
                    self.words_list.append(words[i])

            word_bank = []

            # #Update the word bank
            for file in list_of_files:
                if file == list_of_files[0]:
                    word_bank = self.words_list[0:self.words_list.index(change_files[0]) + 1]
                elif file == list_of_files[1]:
                    word_bank = self.words_list[self.words_list.index(change_files[0]) + 1:self.words_list.index(change_files[1]) + 1]
                elif file == list_of_files[2]:
                    word_bank = self.words_list[self.words_list.index(change_files[1]) + 1:self.words_list.index(change_files[2]) + 1]
                elif file == list_of_files[3]:
                    word_bank = self.words_list[self.words_list.index(change_files[2]) + 1:self.words_list.index(change_files[3]) + 1]
            
                file_path = os.path.join(base_dir, "Word Bank", file)
                with open(file_path, "w", encoding="utf-8") as f:
                    for word in word_bank:         
                        f.write(word)
                    f.write("Challenge complete? No")
                word_bank.clear()

            self.category_frame.place_forget()
            self.difficulty_frame.place_forget()
            self.word_bank_frame.place_forget()
            self.play_button.place_forget()
            self.go_back_button.place_forget()
            self.word_bank_progression()
            self.setup_game_settings_screen()
            messagebox.showinfo("Word Bank Reset", "The Word Bank has been sucessfully reset!")
        else:
            return


    #---> Difficulty & Category Functions

    def change_category(self, new_category):
        self.category_selected = new_category
        self.show_category.set("Category selected -> {}".format(self.category_selected))


    def change_difficulty(self, new_difficulty):
        self.difficulty_selected = new_difficulty
        self.show_difficulty.set("Difficulty selected -> {}".format(self.difficulty_selected))
            

    #---> User info related functions
    def load_user_info(self):
        """
        This function will load the user info from the "user.txt" file
        which contain the difficulty & category that the user previously chose
        """

        # Get the absolute path of the directory where the script is located & csonstruct the full path to the file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "user.txt")

        with open(file_path, "r", encoding="utf-8") as f:
            user_info = f.readlines()

        self.category_selected = user_info[0][9:-1]
        self.difficulty_selected = user_info[1][11:-1]
        self.hints = user_info[2][7:]


    #---> Other functions 
    def difficulty_explanation(self):
        """
        This function will open a new Toplevel window which shows the explanation for each difficulty
        """
        self.difficulty_window = Toplevel()
        self.difficulty_window.title("How to Play?")
        self.difficulty_window.geometry("500x400")
        self.difficulty_window.resizable(False, False)
        self.difficulty_window.config(background="lightgrey")
        from main import AppConfig
        AppConfig.center_window(self.difficulty_window, 500, 400)

        arrow_path = os.path.join("images","arrow4.png")
        arrow = Image.open(arrow_path)
        arrow = arrow.resize((35, 35))
        open_new_img = ImageTk.PhotoImage(arrow)

        # Easy difficulty
        self.easy_lbl = Label(self.difficulty_window, text="Easy", bg="#84f069", fg="white", font=("Helvetica", 22, "bold")).place(x = 100, y = 40)

        self.arrow1_img = Label(self.difficulty_window, bg="lightgrey", image = open_new_img)
        self.arrow1_img.image = open_new_img
        self.arrow1_img.place(x = 200, y = 42)

        self.easy_difficulty_explanation = Label(self.difficulty_window, text="up to 5 letters", bg = "lightgrey", font=("Helvetica", 16)).place(x = 290, y = 45)
        self.easy_difficulty_hints = Label(self.difficulty_window, text = "(1 hint p/word)", bg = "lightgrey", font = ("Helvetica", 12)).place(x = 315, y = 72)

        # Medium difficulty
        self.medium_lbl = Label(self.difficulty_window, text="Medium", bg="#e0e342", fg="white", font=("Helvetica", 22, "bold")).place(x = 58, y = 130)

        self.arrow2_img = Label(self.difficulty_window, bg="lightgrey", image = open_new_img)
        self.arrow2_img.image = open_new_img
        self.arrow2_img.place(x = 200, y = 132)

        self.medium_difficulty_explanation = Label(self.difficulty_window, text="between 6 and 9 letters", bg="lightgrey", font=("Helvetica", 16)).place(x = 255, y = 135)
        self.medium_difficulty_hints = Label(self.difficulty_window, text = "(2 hints p/word)", bg = "lightgrey", font = ("Helvetica", 12)).place(x = 310, y = 157)


        # Hard difficulty
        self.hard_lbl = Label(self.difficulty_window, text="Hard", bg="#de1c07", fg="white", font=("Helvetica", 22, "bold")).place(x = 100, y = 220)

        self.arrow3_img = Label(self.difficulty_window, bg="lightgrey", image = open_new_img)
        self.arrow3_img.image = open_new_img
        self.arrow3_img.place(x = 200, y = 222)

        self.hard_difficulty_explanation = Label(self.difficulty_window, text="+10 letters", bg="lightgrey", font=("Helvetica", 16)).place(x = 300, y = 223)
        self.hard_difficulty_hints = Label(self.difficulty_window, text = "(3 hints p/word)", bg = "lightgrey", font = ("Helvetica", 12)).place(x = 305, y = 245)

        # Challenge difficulty
        self.challenge_lbl = Label(self.difficulty_window, text="Challenge", bg="#751207", fg="white", font=("Helvetica", 22, "bold")).place(x = 25, y = 310)

        self.arrow4_img = Label(self.difficulty_window, bg="lightgrey", image = open_new_img)
        self.arrow4_img.image = open_new_img
        self.arrow4_img.place(x = 200, y = 312)

        self.challenge_difficulty_explanation = Label(self.difficulty_window, text="5 minutes to guess\n 5 'Hard' words", bg="lightgrey", font=("Helvetica", 16)).place(x = 260, y = 300)


    def start_game(self):
        if self.category_selected == "" or self.difficulty_selected == "":
            messagebox.showwarning("Error","You need to select a category and a difficulty to start the game!")
        else:
            # Remove all widgets
            self.category_frame.place_forget()
            self.difficulty_frame.place_forget()
            self.word_bank_frame.place_forget()
            self.play_button.place_forget()
            self.go_back_button.place_forget()
            Game(self.window, self.difficulty_selected, self.category_selected, self.hints, "Classic")


    def go_back(self):
        """
        This function will make the user go back to the
        gamemode selection screen!
        """
        # Remove all widgets
        self.category_frame.place_forget()
        self.difficulty_frame.place_forget()
        self.word_bank_frame.place_forget()
        self.play_button.place_forget()
        self.go_back_button.place_forget()

        from gamemode_screen import GamemodeScreenApp
        GamemodeScreenApp(self.window)



# Flag Mode!
class FlagModeSettings:
    def __init__(self, window):
        self.window = window
        self.hints = 0

        self.load_user_info()
        self.country_bank_progression()
        self.setup_game_settings_screen()


    def setup_game_settings_screen(self):
        """
        This function has all the game setting's widgets!
        """
        # ---> Frames
        self.continents_frame = Frame(self.window, width= 950, height= 410, bg="lightgrey")
        self.continents_frame.place(x = 25, y = 60)

        self.country_bank_frame = Frame(self.window, width=950, height=250, bg="lightgrey")
        self.country_bank_frame.place(x = 25, y = 520)

        # ---> Go back button
        icon_path = os.path.join("images","go_back_icon.png")
        icon = Image.open(icon_path)
        icon = icon.resize((44, 44))
        open_new_icon = ImageTk.PhotoImage(icon)
        self.go_back_button = Button(self.window, image=open_new_icon, bg="lightgrey", command = lambda: self.go_back())
        self.go_back_button.image = open_new_icon
        self.go_back_button.place(x = 920, y = 5)

        # ---> Labels
        self.choose_continent_lbl = Label(self.window, text = "Choose a continent!", bg="lightgrey", font=("Arial", 24, "bold"))
        self.choose_continent_lbl.place(x = 370, y = 10)

        self.word_bank_progression_lbl = Label(self.window, text = "Word Bank Progression", bg = "lightgrey", font=("Arial", 24, "bold"))
        self.word_bank_progression_lbl.place(x = 335, y = 475)

        # ---> Continent Frame Widgets
        # ---> Continent Labels
        self.europe_lbl = Label(self.continents_frame, text = "Europe", font = ("Arial", 18, "bold"), bg = "lightgrey")
        self.america_lbl = Label(self.continents_frame, text = "America", font = ("Arial", 18, "bold"), bg = "lightgrey")
        self.asia_lbl = Label(self.continents_frame, text = "Asia", font = ("Arial", 18, "bold"), bg = "lightgrey")
        self.africa_lbl = Label(self.continents_frame, text = "Africa", font = ("Arial", 18, "bold"), bg = "lightgrey")
        self.oceania_lbl = Label(self.continents_frame, text = "Oceania", font = ("Arial", 18, "bold"), bg = "lightgrey")
        
        self.europe_lbl.place(x = 90, y = 5)
        self.america_lbl.place(x = 440, y = 5)
        self.asia_lbl.place(x = 785, y = 5)
        self.africa_lbl.place(x = 285, y = 195)
        self.oceania_lbl.place(x = 600, y = 195)


        # ---> Button Images
        europe_icon_path = os.path.join("images", "flag_gamemode", "continent_icons", "europe_icon.png")
        europe_icon = Image.open(europe_icon_path)
        europe_icon = europe_icon.resize((150, 150))
        open_europe_icon = ImageTk.PhotoImage(europe_icon)

        america_icon_path = os.path.join("images", "flag_gamemode", "continent_icons", "america_icon.png")
        america_icon = Image.open(america_icon_path)
        america_icon = america_icon.resize((150, 150))
        open_america_icon = ImageTk.PhotoImage(america_icon)

        asia_icon_path = os.path.join("images", "flag_gamemode", "continent_icons", "asia_icon.png")
        asia_icon = Image.open(asia_icon_path)
        asia_icon = asia_icon.resize((150, 150))
        open_asia_icon = ImageTk.PhotoImage(asia_icon)

        africa_icon_path = os.path.join("images", "flag_gamemode", "continent_icons", "africa_icon.png")
        africa_icon = Image.open(africa_icon_path)
        africa_icon = africa_icon.resize((150, 150))
        open_africa_icon = ImageTk.PhotoImage(africa_icon)

        oceania_icon_path = os.path.join("images", "flag_gamemode", "continent_icons", "oceania_icon.png")
        oceania_icon = Image.open(oceania_icon_path)
        oceania_icon = oceania_icon.resize((150, 150))
        open_oceania_icon = ImageTk.PhotoImage(oceania_icon)


        # ---> Button Widgets
        self.europe_button = Button(self.continents_frame, image=open_europe_icon, bg = "#bcf6f0", width = 175, height= 150, border = 2, command = lambda: self.start_game("Europe"))
        self.america_button = Button(self.continents_frame, image=open_america_icon, bg = "#f8cb76", width = 175, height= 150, border = 2, command = lambda: self.start_game("America"))
        self.asia_button = Button(self.continents_frame, image=open_asia_icon, bg = "#f77070", width = 175, height= 150, border = 2, command = lambda: self.start_game("Asia"))
        self.africa_button = Button(self.continents_frame, image=open_africa_icon, bg = "#a7f770", width = 175, height= 150, border = 2, command = lambda: self.start_game("Africa"))
        self.oceania_button = Button(self.continents_frame, image=open_oceania_icon, bg = "#70f7c4", width = 175, height= 150, border = 2, command = lambda: self.start_game("Oceania"))

        self.europe_button.image = open_europe_icon
        self.america_button.image = open_america_icon
        self.asia_button.image = open_asia_icon
        self.africa_button.image = open_africa_icon
        self.oceania_button.image = open_oceania_icon

        self.europe_button.place(x = 50, y = 40)
        self.america_button.place(x = 400, y = 40)
        self.asia_button.place(x = 720, y = 40)
        self.africa_button.place(x = 230, y = 230)
        self.oceania_button.place(x = 560, y = 230)


        # ---> Word Bank Progression Frame Widgets
        self.total_words_lbl = Label(self.country_bank_frame, text = "Total Countries found: {}/{}".format(self.total_countries_found, self.total_countries), font = ("Arial", 18, "bold"), bg = "lightgrey")
        self.european_countries_lbl = Label(self.country_bank_frame, text = "European\n Countries found:\n{}/{}".format(self.european_countries_found, self.european_countries), font = ("Arial", 16), bg = "#bcf6f0")
        self.american_countries_lbl = Label(self.country_bank_frame, text = "American\n Countries found:\n{}/{}".format(self.american_countries_found, self.american_countries), font = ("Arial", 16), bg = "#f8cb76")
        self.asian_countries_lbl = Label(self.country_bank_frame, text = "Asian\n Countries found:\n{}/{}".format(self.asian_countries_found, self.asian_countries), font = ("Arial", 16), bg = "#f77070")
        self.african_countries_lbl = Label(self.country_bank_frame, text = "African\n Countries found:\n{}/{}".format(self.african_countries_found, self.african_countries), font = ("Arial", 16), bg = "#a7f770")
        self.oceanian_countries_lbl = Label(self.country_bank_frame, text = "Oceanian\n Countries found:\n{}/{}".format(self.oceanian_countries_found, self.oceanian_countries), font = ("Arial", 16), bg = "#70f7c4")
        self.reset_word_bank_btn = Button(self.country_bank_frame, text="Reset Word Bank", font=("Arial", 14), border=2 , width=15, height=1, command=lambda: self.reset_country_bank())

        self.total_words_lbl.place(x = 330, y = 10)
        self.european_countries_lbl.place(x = 10, y = 70)
        self.american_countries_lbl.place(x = 200, y = 70)
        self.asian_countries_lbl.place(x = 390, y = 70)
        self.african_countries_lbl.place(x = 580, y = 70)
        self.oceanian_countries_lbl.place(x = 770, y = 70)
        self.reset_word_bank_btn.place(x = 750, y = 10)



    # --> Country Bank Functions
    
    def country_bank_progression(self):
        """
        This function has several functionalities which mostly tells the user their progression on the game
        It mostly counts the total words the user found and how many words there are still to find for each
        continent
        """
        self.countries_list = []
        self.total_countries = 0
        self.total_countries_found = 0
        self.european_countries = 0
        self.european_countries_found = 0
        self.american_countries = 0
        self.american_countries_found = 0
        self.asian_countries = 0
        self.asian_countries_found = 0
        self.african_countries = 0
        self.african_countries_found = 0
        self.oceanian_countries = 0
        self.oceanian_countries_found = 0

        base_dir = os.path.dirname(os.path.abspath(__file__))
        list_of_files = ["europe.txt","america.txt","asia.txt","africa.txt","oceania.txt"]

        #--> Add all countries to the countries_list array
        for file in list_of_files:
            file_path = os.path.join(base_dir, "Word Bank", "flag_gamemode", file)

            with open(file_path, "r", encoding = "utf-8") as f:
                countries = f.readlines()

            for country in countries:
                self.total_countries += 1

                if ";guessed" in country:
                    self.total_countries_found += 1

                if file == "europe.txt":
                    self.european_countries += 1
                    
                    if ";guessed" in country:
                        self.european_countries_found += 1
                elif file == "america.txt":
                    self.american_countries += 1

                    if ";guessed" in country:
                        self.american_countries_found += 1
                elif file == "asia.txt":
                    self.asian_countries += 1

                    if ";guessed" in country:
                        self.asian_countries_found += 1
                elif file == "africa.txt":
                    self.african_countries += 1

                    if ";guessed" in country:
                        self.african_countries_found += 1
                elif file == "oceania.txt":
                    self.oceanian_countries += 1

                    if ";guessed" in country:
                        self.oceanian_countries_found += 1

    def reset_country_bank(self):
        
        answer = messagebox.askquestion("Reset Word Bank", 
                               "Are you sure? If so, all the progression you've made will be reset and all the words you found can be selected again for you to guess!")

        if answer == "yes":
            self.countries_list = []

            base_dir = os.path.dirname(os.path.abspath(__file__))
            list_of_files = ["europe.txt","america.txt","asia.txt","africa.txt","oceania.txt"]
            change_files = []

            #--> Add all countries to the countries_list array
            for file in list_of_files:
                file_path = os.path.join(base_dir, "Word Bank", "flag_gamemode", file)

                with open(file_path, "r", encoding = "utf-8") as f:
                    countries = f.readlines()

                for i in range (len(countries)):
                    if ";guessed" in countries[i]:
                        countries[i] = countries[i][0:countries[i].find(";")]
                        if countries[i] != countries[len(countries) - 1]:
                            countries[i] = countries[i] + "\n"
                    if countries[i] == countries[len(countries) - 1]:
                        change_files.append(countries[i])
                    self.countries_list.append(countries[i])

            country_bank = []

            #Update the country bank
            for file in list_of_files:
                if file == list_of_files[0]:
                    country_bank = self.countries_list[0:self.countries_list.index(change_files[0]) + 1]
                elif file == list_of_files[1]:
                    country_bank = self.countries_list[self.countries_list.index(change_files[0]) + 1: self.countries_list.index(change_files[1]) + 1]
                elif file == list_of_files[2]:
                    country_bank = self.countries_list[self.countries_list.index(change_files[1]) + 1: self.countries_list.index(change_files[2]) + 1]
                elif file == list_of_files[3]:
                    country_bank = self.countries_list[self.countries_list.index(change_files[2]) + 1: self.countries_list.index(change_files[3]) + 1]
                elif file == list_of_files[4]:
                    country_bank = self.countries_list[self.countries_list.index(change_files[3]) + 1: self.countries_list.index(change_files[4]) + 1]

                file_path = os.path.join(base_dir, "Word Bank", "flag_gamemode", file)
                with open(file_path, "w", encoding="utf-8") as f:
                    for country in country_bank:
                        f.write(country)
                country_bank.clear()


            self.continents_frame.place_forget()
            self.country_bank_frame.place_forget()
            self.go_back_button.place_forget()
            self.choose_continent_lbl.place_forget()
            self.word_bank_progression_lbl.place_forget()
            self.country_bank_progression()
            self.setup_game_settings_screen()
            messagebox.showinfo("Word Bank Reset", "The Word Bank has been sucessfully reset!")
        else:
            return

    #---> Other functions
    def start_game(self, category):
        self.continents_frame.place_forget()
        self.country_bank_frame.place_forget()
        self.go_back_button.place_forget()
        self.choose_continent_lbl.place_forget()
        self.word_bank_progression_lbl.place_forget()

        Game(self.window, "", category, self.hints, "Flag")

    def load_user_info(self):
        """
        This function will load the user info from the "user.txt" file
        which contain the difficulty & category that the user previously chose
        """

        # Get the absolute path of the directory where the script is located & csonstruct the full path to the file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "user.txt")

        with open(file_path, "r", encoding="utf-8") as f:
            user_info = f.readlines()

        self.hints = user_info[2][7:]

    def go_back(self):
        """
        This function will make the user go back to the
        gamemode selection screen!
        """
        self.continents_frame.place_forget()
        self.country_bank_frame.place_forget()
        self.go_back_button.place_forget()
        self.choose_continent_lbl.place_forget()
        self.word_bank_progression_lbl.place_forget()

        from gamemode_screen import GamemodeScreenApp
        GamemodeScreenApp(self.window)

