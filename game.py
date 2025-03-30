from tkinter import *
from tkinter import messagebox
import os
from PIL import Image, ImageTk
import random
    
class Game:
    def __init__(self, window, difficulty, category, hints, gamemode):
        self.window = window
        self.difficulty = difficulty #--> Difficulty chosen (if applied)
        self.category = category #--> Category chosen
        self.hints = int(hints) #-->Nº of hints the user has
        self.hints_limit = 0 #--> The limit of hints for each difficulty
        self.hint_storage = [] #--> Stores all hints used
        self.gamemode = gamemode #--> Gamemode chosen
        self.popup = None #--> Add/remove a popup
        self.x_position = 0 
        self.tries = 5
        self.input_area = ""
        self.chosen_word = "" #--> Secret word
        self.label_color = "" #--> Label color for difficulty (each difficulty has their own label color)
        #---> Challenge-related variables
        self.challenge_words = [] #--> To store all chosen words for the challenge
        self.word_counter = 1 #--> To count the amount of words the user guessed
        #Timer variables for "Challenge" difficulty
        self.minutes_timer = 5
        self.seconds_timer = 1
        if self.difficulty == "Easy":
            self.hints_limit = 1
        elif self.difficulty == "Medium":
            self.hints_limit = 2
        elif self.difficulty == "Hard" or self.difficulty == "Challenge":
            self.hints_limit = 3 
        if self.gamemode == "Classic":
            self.save_user_info()
            self.select_word()
        elif self.gamemode == "Flag":
            self.hints_limit = 3
            self.select_country()

    #-------> Game Screen Widgets!
    def screen_setup(self, chosen_difficulty, minutes_timer, seconds_timer):
        """
        This function has all the game screen's widgets!
        """
        self.y_position = 200

        self.game_frame = Frame(self.window, width=950, height=680, bg="lightgrey")
        self.game_frame.place(x = 25, y = 10)

        #--> Go back button
        icon_path = os.path.join("images","go_back_icon.png")
        icon = Image.open(icon_path)
        icon = icon.resize((56, 56))
        open_new_icon = ImageTk.PhotoImage(icon)
        self.go_back_button = Button(self.game_frame, image=open_new_icon, bg="lightgrey", command=lambda: (self.return_to_title_screen()))
        self.go_back_button.image = open_new_icon
        self.go_back_button.place(x = 850, y = 10)

        #--> Skip Word button
        icon_path2 = os.path.join("images","skip_icon.png")
        icon2 = Image.open(icon_path2)
        icon2 = icon2.resize((56, 56))
        open_new_icon2 = ImageTk.PhotoImage(icon2)
        if self.difficulty == "Challenge":
            self.skip_button = Button(self.game_frame, image=open_new_icon2, bg="lightgrey", state = "disabled", command=lambda: (self.play_again()))
        else:
            self.skip_button = Button(self.game_frame, image=open_new_icon2, bg="lightgrey", command=lambda: (self.play_again()))
        self.skip_button.image = open_new_icon2
        self.skip_button.place(x = 850, y = 600)

        #--> Hint button Image
        icon_path3 = os.path.join("images","hint_icon.png")
        icon3 = Image.open(icon_path3)
        icon3 = icon3.resize((56, 56))
        self.open_new_icon3 = ImageTk.PhotoImage(icon3)
        if self.hints > 0:
            self.hints_button = Button(self.game_frame, image=self.open_new_icon3, bg="lightgrey", command=lambda: (self.use_hint()))
            self.hints_button.image = self.open_new_icon3
            self.hints_button.place(x = 780, y = 600)
        else:
            self.hints_button = Button(self.game_frame, image=self.open_new_icon3, bg="lightgrey", state = "disabled")
            self.hints_button.image = self.open_new_icon3
            self.hints_button.place(x = 780, y = 600)


        self.show_tries_text = StringVar()
        self.show_tries_text.set("Tries Left -> {}".format(self.tries))
        self.show_tries = Label(self.game_frame, bg="lightgrey", textvariable = self.show_tries_text, font=("Arial", 22))
        self.show_tries.place(x = 380, y = 50)

        self.category_chosen = Label(self.game_frame, bg="lightgrey", text="{}".format(self.category), font=("Arial", 20))
        self.category_chosen.place(x = self.category_label_x_pos, y = 10)

        entryWidth = 2
        secret_word = ""
        if self.gamemode == "Classic":
            entryWidth += len(self.chosen_word.replace(" ",""))
        else:
            entryWidth += len(self.chosen_country.replace(" ",""))
        self.user_guess = StringVar()
        self.user_guess.set("")
        self.insert_guess = Entry(self.game_frame, textvariable=self.user_guess, bg="white", font=("Arial", 20), width=entryWidth)
        self.insert_guess.place(x = self.calculate_center_frame(secret_word, 20) - 100, y = 550)
        self.insert_guess.bind("<KeyRelease>", self.limit_number_chars)
        
        self.guess_label = Label(self.game_frame, bg = "lightgrey", text = "Your guess:", font=("Arial", 20)).place(x = self.calculate_center_frame("Your guess:", 20) - 100, y = 550)
        self.submit_label = Label(self.game_frame, bg = "lightgrey", text = "[Press 'Enter' to submit!]", font = ("Arial", 14)).place(x = self.calculate_center_frame("[Press 'Enter' to submit!]", 14), y = 590)

        self.hints_number = StringVar()
        self.hints_number.set("{}".format(self.hints))
        self.hints_number_label = Label(self.game_frame, bg = "lightgrey", textvariable = self.hints_number, font = ("Arial", 22)).place(x = 760, y = 570)

        #--> Bind the <Enter> button to submit an answer
        self.window.bind("<Return>", lambda event: self.check_answer())
        self.display_first_label()

        if self.gamemode == "Classic":
            self.minutes_timer = minutes_timer
            self.seconds_timer = seconds_timer

            self.difficulty_chosen = Label(self.game_frame, bg= self.label_color, text="{}".format(chosen_difficulty), fg="white", font=("Arial", 20, "bold"))
            self.difficulty_chosen.place(x = self.difficulty_label_x_pos, y = 90)

            if self.difficulty == "Challenge":
                self.timer = Label(self.game_frame, bg="lightgrey", text="{}:{}".format(self.minutes_timer, self.seconds_timer), font=("Arial", 22, "bold"))
                self.timer.place(x = 420, y = 140)
                self.set_timer(self.minutes_timer, self.seconds_timer)
        else:
            flag_path = os.path.join(self.folder_path, self.chosen_country_flag)
            flag = Image.open(flag_path)
            flag = flag.resize((130, 90))
            open_flag = ImageTk.PhotoImage(flag)
            self.flag_image = Label(self.game_frame, image = open_flag, bg = "lightgrey")
            self.flag_image.image = open_flag
            self.flag_image.place(x = 400, y = 100)


    #-------> Game Management
    def select_word(self):
        """
        Based on the category chosen by the user, 
        a random word is picked from the chosen category
        """
        # Initialize the "file_name" and "category" variables based on the category chosen
        file_name = ""

        # Get the absolute path of the directory where the script is located
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Check which category the user chose and open the respective word bank
        if self.category == "Animals":
            file_name = "animals.txt" 
            self.category_label_x_pos = 400
        elif self.category == "Fruits":
            file_name = "fruits.txt"
            self.category_label_x_pos = 415
        elif self.category == "Colors":
            file_name = "colors.txt"
            self.category_label_x_pos = 410
        elif self.category == "Jobs":
            file_name = "jobs.txt"
            self.category_label_x_pos = 420

        # Construct the full path to the file
        self.file_path = os.path.join(base_dir, "Word Bank", file_name)

        # Open the file using the absolute path
        with open(self.file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            lines.pop()
        word_bank = []

        # Checks for already guessed words!
        for line in lines:
            line = line.rstrip("\n")
            if ";guessed" not in line:
                word_bank.append(line)

            if self.difficulty == "Challenge":
                if ";guessed" in line:
                    word_bank.append(line[:-8])
                else:
                    word_bank.append(line)

        # Picks a random word
        self.chosen_word = word_bank[random.randint(0, len(word_bank) - 1)].upper()
    
        chosen_difficulty = self.difficulty

        # If the difficulty is "Random"
        if chosen_difficulty == "Random":
            difficulties = ["Easy","Medium","Hard"]
            chosen_difficulty = difficulties[random.randint(-1, 2)]

        #Check if there are words within the difficulty & category chosen
        if chosen_difficulty != "Challenge":
            words_available = False
            for word in word_bank:
                if chosen_difficulty == "Easy":
                    if len(word) <= 5:
                        words_available = True
                elif chosen_difficulty == "Medium":
                    if len(word) >= 6 and len(word) <= 9:
                        words_available = True
                elif chosen_difficulty == "Hard":
                    if len(word) >= 10:
                        words_available = True

            if words_available == False:
                messagebox.showinfo("All words found!","All words were found for the {} difficulty in the {} category!\n Try to choose a different category and/or difficulty!" .format(chosen_difficulty, self.category))
                from game_settings_screen import ClassicModeSettings
                ClassicModeSettings(self.window)
                return

        #Pick a word that has the parameters of the selected difficulty
        if chosen_difficulty == "Easy":
            self.label_color = "#84f069"
            self.difficulty_label_x_pos = 420
            while len(self.chosen_word) > 5:
                self.chosen_word = word_bank[random.randint(0, len(word_bank) - 1)].upper()
        elif chosen_difficulty == "Medium":
            self.label_color = "#e0e342"
            self.difficulty_label_x_pos = 400
            while len(self.chosen_word) < 6 or len(self.chosen_word) > 9:
                self.chosen_word = word_bank[random.randint(0, len(word_bank) - 1)].upper()
        elif chosen_difficulty == "Hard":
            self.label_color = "#de1c07"
            self.difficulty_label_x_pos = 420
            while len(self.chosen_word) < 10:
                self.chosen_word = word_bank[random.randint(0, len(word_bank) - 1)].upper()
        elif chosen_difficulty == "Challenge":
            self.label_color = "#751207"
            self.difficulty_label_x_pos = 380
            # Picks 5 random Hard words and adds them into the "challenged_words" array
            for i in range (5):
                while len(self.chosen_word) < 10 or self.chosen_word in self.challenge_words:
                        self.chosen_word = word_bank[random.randint(0, len(word_bank) - 1)].upper()
                self.challenge_words.append(self.chosen_word)
                self.chosen_word = self.challenge_words[0]

        #("The chosen word is -> {}\n".format(self.chosen_word))
        self.screen_setup(chosen_difficulty, self.minutes_timer, self.seconds_timer)


    def select_country(self):
        """
        Based on the continent chosen by the user, 
        a random word is picked from that chosen continent
        """

        folder_name = "" # --> This variable will contain the folder's name depending on which continent the player chose!

        base_dir = os.path.dirname(os.path.abspath(__file__)) # --> Absolute path for the script directory

        if self.category == "Europe":
            folder_name = "europe"
            self.category_label_x_pos = 425
            self.category_label_color = "#bcf6f0"

        elif self.category == "America":
            folder_name = "america"
            self.category_label_x_pos = 410
            self.category_label_color = "#f8cb76"

        elif self.category == "Asia":
            folder_name = "asia"
            self.category_label_x_pos = 440
            self.category_label_color = "#f77070"

        elif self.category == "Africa":
            folder_name = "africa"
            self.category_label_x_pos = 430
            self.category_label_color = "#a7f770"

        elif self.category == "Oceania":
            folder_name = "oceania"
            self.category_label_x_pos = 420
            self.category_label_color = "#70f7c4"

        # --> Construct the full path to the wanted folder
        self.folder_path = os.path.join(base_dir, "images", "flag_gamemode", "country_icons", folder_name)

        # --> To position in the continent folder containing all flag images
        os.chdir(self.folder_path)

        # --> This array will contain all flag images
        countries_image_list = os.listdir()
        
        # --> Add the file name for the chosen continent
        self.file_path = os.path.join(base_dir, "Word Bank", "flag_gamemode", folder_name)
        self.file_path = self.file_path + ".txt"

        with open(self.file_path, "r", encoding = "utf-8") as f:
            lines = f.readlines()


        country_bank = []

        # Already guessed words won't be picked again! (Unless the user resets the Word Bank)
        for line in lines:
            line = line.rstrip("\n")
            if ";guessed" not in line:
                country_bank.append(line)
            else:
                
                line = line[:-8]
                line = line.lower()
                if line.find(" "):
                    line = line.replace(" ", "-")
                countries_image_list.remove(line + ".png")

        if len(country_bank) == 0:
            messagebox.showinfo("All words found!","All countries were found for {}!" .format(self.category))
            from game_settings_screen import FlagModeSettings
            os.chdir('..\\..')
            os.chdir('..\\..')
            FlagModeSettings(self.window)
            return

        random_index = random.randint(0, len(country_bank) - 1)
        self.chosen_country = country_bank[random_index].upper()
        self.chosen_country_flag = countries_image_list[random_index]

        #print("The chosen country is -> {}\n" .format(self.chosen_country))
        os.chdir('..\\..')
        os.chdir('..\\..')
        self.screen_setup("", 0, 0)
            

    def display_first_label(self):
        """
        This function will render a row of entry boxes where the user can submit their guess
        This function is first called when the game screen is created as well as everytime the user submits a guess
        """
        secret_word = ""
        if self.gamemode == "Classic":
            secret_word = self.chosen_word
        else:
            secret_word = self.chosen_country

        if len(secret_word) <= 5:
                self.x_position = self.calculate_center_frame(secret_word, 28) - 100
        elif len(secret_word) >= 6 and len(secret_word) < 9:
                self.x_position = self.calculate_center_frame(secret_word, 28) - 150
        elif len(secret_word) >= 9:
                self.x_position = self.calculate_center_frame(secret_word, 28) - 250

        for i, char in enumerate(secret_word):
            if char != " ":
                new_label = Label(self.game_frame, bg = "white", font = ("Arial", 28), text = " ", width = 2) 
                new_label.place(x = self.x_position, y = self.y_position)
            self.x_position += 55
    

    def use_hint(self):
        self.hints -= 1
        self.hints_limit -= 1
        secret_word = ""
        if self.gamemode == "Classic":
            secret_word = self.chosen_word
        else:
            secret_word = self.chosen_country
            
        #--> Choose a random letter index to be revealed
        random_index = random.randint(0, len(secret_word) - 1)
        while random_index in self.hint_storage or secret_word[random_index] == " ":
            random_index = random.randint(0, len(secret_word) - 1)

        #--> Append that index to a storage so all the hints will always appear
        self.hint_storage.append(random_index)        

        #--> Check what letters will be revealed depending on their index and whether or not they're in the hints_storage
        self.x_position = self.calculate_center_frame(secret_word, 28)
        for i, letter in enumerate(secret_word):
            if letter == " ":
                self.x_position += 55
            elif i not in self.hint_storage:
                new_label = Label(self.game_frame, bg = "white", font = ("Arial", 28), text = " ", width = 2) 
                new_label.place(x = self.x_position, y = self.y_position)
                self.x_position += 55
            else:
                self.render_result("green", letter)
                self.x_position += 55

        #--> Disable the button if there are no more hints or the hint limit was surpassed
        if self.hints == 0 or self.hints_limit == 0:
            self.hints_button.place_forget()
            self.hints_button = Button(self.game_frame, image=self.open_new_icon3, bg="lightgrey", state="disabled")
            self.hints_button.image = self.open_new_icon3
            self.hints_button.place(x = 780, y = 600)

        #--> Update the nº of hints
        self.hints_number.set("{}".format(self.hints))
        self.save_user_info()


    def set_timer(self, minutes_timer, seconds_timer):
        self.minutes_timer = minutes_timer
        self.seconds_timer = seconds_timer

        self.seconds_timer -= 1
        if self.seconds_timer == 0:
            if self.minutes_timer == 0:
                messagebox.showwarning("Game's over","Time's up! :(")
                self.return_to_title_screen()
                return
            self.seconds_timer = 59
            self.minutes_timer -= 1
        
        if self.seconds_timer < 10:
            self.timer.config(text = "{}:0{}".format(self.minutes_timer, self.seconds_timer))
        else:
            self.timer.config(text = "{}:{}".format(self.minutes_timer, self.seconds_timer))

        self.timer_id = self.window.after(1000, lambda: self.set_timer(self.minutes_timer, self.seconds_timer))


    def stop_timer(self):
        """
        This function will stop the set_timer() function once the user guesses a word
        If this function wasn't here, there would be for example 2 timers running in the 
        2nd mysterious word
        """
        if self.timer_id:
            self.window.after_cancel(self.timer_id)
            self.timer_id = None

    #----> Input Functionalities
    def limit_number_chars(self, event):
        """
        This function prevents the user from typing more than 1 char in a Entry box

        """
        entry = event.widget

        # Delete the extra chars 
        n_chars = len(entry.get())
        if self.gamemode == "Classic":
            if (n_chars > len(self.chosen_word)):
                entry.delete(n_chars - 1, END)
        else:
            if (n_chars > len(self.chosen_country)):
                entry.delete(n_chars - 1, END)
            
            
    def calculate_center_frame(self, text_length, font_size):
        """
        This function center the "game_frame" Frame vertically 
        based on the length & font size of the element that calls this function
        """
        text_width = len(text_length) * font_size
        return  (1000 - text_width) / 2

    #----> Check user's answer
    def check_answer(self):
        """
        Once the user submits their guess, this function will check which
        letters are in the correct position (green bg),
        which are in the wrong position (yellow bg),
        and which aren't in the secret word at all (grey bg)
        """
        new_guess = self.user_guess.get()
        new_guess = new_guess.upper()
        new_guess = new_guess.replace(" ", "")
        # Remove a space when there is one so the secret word's length isn't interfered by the space 
        if self.gamemode == "Classic":
            secret_word = self.chosen_word.replace(" ","") 
        else:
            secret_word = self.chosen_country.replace(" ","") 

        if len(secret_word) <= 5:
                self.x_position = self.calculate_center_frame(secret_word, 28) - 100
        elif len(secret_word) >= 6 and len(secret_word) < 9:
                self.x_position = self.calculate_center_frame(secret_word, 28) - 150
        elif len(secret_word) >= 9:
                self.x_position = self.calculate_center_frame(secret_word, 28) - 250

        self.y_position += 60
        self.user_guess.set("")

        # Check if the nª of letters of the user's guess and the secret word are the same!
            # Check if the letter is in the word
        for i, letter in enumerate(new_guess):
            if self.gamemode == "Classic":
                if self.chosen_word[i] == " ":
                    self.x_position += 55
                # If the letter is correct and the position where that letter is supposed to be already has that letter
                if letter in secret_word and letter != secret_word[i]:
                    for j in range (len(secret_word)):
                        if new_guess[j] == new_guess[i] and new_guess[j] == secret_word[j]:
                            self.render_result("lightgrey", letter)
                            break
                        if j == (len(secret_word) - 1):
                            # The letter is in the word, but in the wrong position
                            self.render_result("yellow", letter)
                elif letter == secret_word[i] or letter in self.hint_storage:
                    # The letter is in the word as well as in the correct position
                    self.render_result("green", letter)
                else:
                    # The letter isn't in the word
                    self.render_result("lightgrey", letter)
                self.x_position += 55
            else:
                if self.chosen_country[i] == " ":
                    self.x_position += 55
                if letter in secret_word and letter != secret_word[i]:
                    # If the letter is correct and the position where that letter is supposed to be already has that letter
                    for j in range (len(secret_word)):
                        if new_guess[j] == new_guess[i] and new_guess[j] == secret_word[j]:
                            self.render_result("lightgrey", letter)
                            break
                        if j == (len(secret_word) - 1):
                            # The letter is in the word, but in the wrong position
                            self.render_result("yellow", letter)
                elif letter == secret_word[i]:
                    # The letter is in the word as well as in the correct position
                    self.render_result("green", letter)
                else:
                    #The letter isn't in the word
                    self.render_result("lightgrey", letter)
                self.x_position += 55
                
        if new_guess == secret_word: 
            if self.difficulty == "Challenge":
                if self.word_counter == 5:
                    # Challenge completed!
                    messagebox.showinfo("WOOO","CONGRATS, YOU DID IT! :D")
                    self.update_word_bank()
                    self.save_user_info()
                    self.return_to_title_screen()
                    return
                else:
                    # One step closer to complete the challenge!
                    messagebox.showinfo("Good job!","{} word(s) found! Way to go! :D".format(self.word_counter))
                    self.word_counter += 1
                    self.tries = 5
                    self.stop_timer()
                # Choose a new word
                self.chosen_word = self.challenge_words[self.word_counter - 1]
                self.game_frame.place_forget()
                self.screen_setup(self.difficulty, self.minutes_timer, self.seconds_timer)
            else:
                messagebox.showinfo("CONGRATS!", "YOU GOT IT RIGHT!")
        
                if self.gamemode == "Classic":
                    if self.difficulty == "Easy":
                        self.hints += 1
                    elif self.difficulty == "Medium":
                        self.hints += 2
                    elif self.difficulty == "Hard":
                        self.hints += 3
                    self.update_word_bank()
                else:
                    self.hints += 2
                    self.update_country_bank()

                self.save_user_info()
                self.play_again()
        else:
            if self.tries > 1:
                self.tries-=1
                self.show_tries_text.set("Tries left -> {}".format(self.tries))
            else: 
                self.losing_popup()
                return

    
    def render_result(self, color, letter):
        """
        This function will render the result of the user's guess
        """
        if color == "green":
            letter_result = Label(self.game_frame, bg = "#77d442", font = ("Arial", 28), fg = "white", text = letter, width = 2)
            letter_result.place(x = self.x_position, y = self.y_position)
        elif color == "yellow":
            letter_result = Label(self.game_frame, bg = "#ebf739", font = ("Arial", 28), fg = "white",  text = letter, width = 2)
            letter_result.place(x = self.x_position, y = self.y_position)
        else:
            letter_result = Label(self.game_frame, bg = "lightgrey", font = ("Arial", 28),  text = letter, width = 2)
            letter_result.place(x = self.x_position, y = self.y_position)

    #----> After game ending
    def update_word_bank(self):
        """
        By guessing a word, that word will not appear anymore as long as the user doesn't reset the word bank
        So the word won't appear more times
        """

        with open(self.file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        word_bank = [line.rstrip("\n") for line in lines]

        del word_bank[len(word_bank) - 1] #Delete the last line which is the "Challenge complete?" line

        #Iterate the word bank to update the secret word so it doesn't get chosen again
        for i in range(len(word_bank)):
            if word_bank[i].upper() == self.chosen_word:
                word_bank[i] += ";guessed"  
                
        
        with open(self.file_path, "w", encoding="utf-8") as f:
            for word in word_bank:
                f.write(word + "\n")
            if self.word_counter == 5:
                f.write("Challenge complete? Yes")
            else:
                f.write("Challenge complete? No")
                

    def update_country_bank(self):
        with open(self.file_path, "r", encoding = "utf-8") as f:
            lines = f.readlines()

        country_bank = [line.rstrip("\n") for line in lines]

        #Iterate the country bank to update it
        for i in range(len(country_bank)):
            if country_bank[i].upper() == self.chosen_country:
                country_bank[i] += ";guessed"

        with open(self.file_path, "w", encoding = "utf-8") as f:
            for country in country_bank:
                if country == country_bank[len(country_bank) - 1]:
                    f.write(country)
                else:
                    f.write(country + "\n")
                

    def save_user_info(self):
        """
        This function will update the user's info (what category & difficulty they chose, and nº of hints they have)
        in the "user.txt"
        """

        # Get the absolute path of the directory where the script is located & csonstruct the full path to the file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "user.txt")

        if self.gamemode == "Classic":
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("Category:{}\n" .format(self.category))
                f.write("Difficulty:{}\n".format(self.difficulty))
                f.write("Hints: {}".format(self.hints))
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                user_info = f.readlines()

                category_selected = user_info[0][9:-1]
                difficulty_selected = user_info[1][11:-1]
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("Category:{}\n" .format(category_selected))
                f.write("Difficulty:{}\n".format(difficulty_selected))
                f.write("Hints: {}".format(self.hints))


    def return_to_title_screen(self):
        if self.popup is not None:
            self.popup.destroy()

        self.game_frame.place_forget()
        if self.gamemode == "Classic":
            self.save_user_info()

        if self.gamemode == "Classic":
            from game_settings_screen import ClassicModeSettings
            ClassicModeSettings(self.window)
        else:
            from game_settings_screen import FlagModeSettings
            FlagModeSettings(self.window)


    def play_again(self):
        """
        Keep playing the game (same category and difficulty chosen!).
        """
        if self.popup is not None:
            self.popup.destroy()

        self.game_frame.place_forget()
        Game(self.window, self.difficulty, self.category, self.hints, self.gamemode)
    

    def losing_popup(self):
        """
        This function will display a "popup" showing the user that they spent
        all tries as well as the correct answer
        It also gives the user the possibility to go back to the title screen
        or keep playing!
        """
        self.popup = Toplevel()
        self.popup.title("You lost! :(")
        self.popup.geometry("500x300")
        self.popup.resizable(False, False)
        self.popup.config(background="lightgrey")
        from main import AppConfig
        AppConfig.center_window(self.popup, 500, 300)

        losing_message_lbl = Label(self.popup, text="You lost! :(", font = ("Arial", 18), bg="lightgrey")
        losing_message_lbl.place(x = 190, y = 20)

        go_back_btn = Button(self.popup, text = "Return to \n Title Screen!",width= 12, height=3, font=("Arial", 12), command=lambda:self.return_to_title_screen())
        go_back_btn.place(x = 100, y = 150)

        play_again_btn = Button(self.popup, text="Play again!",width= 12, height=3, font=("Arial", 12), command=lambda:self.play_again())
        play_again_btn.place(x = 300, y = 150)
        