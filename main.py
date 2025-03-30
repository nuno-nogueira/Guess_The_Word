from tkinter import Tk
from welcome_screen import WelcomeScreenApp

class AppConfig:
    window_width = 1000
    window_height = 700
    bg_color = "grey"
    title = "Guess The Word!"

    def center_window(window, width, height):
        """
        This function will center the window based on 
        the screen's width and height! 
        """

        # Get the screen's width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Calculate the x and y coordinates to center the application's screen
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Set the window's geometry with the window's height, width and its x and y coordinates
        window.geometry("{}x{}+{}+{}".format(width, height, x, y))


if __name__ == "__main__":
    window = Tk()
    window.title(AppConfig.title)
    window.configure(bg=AppConfig.bg_color)

    # Center the window
    AppConfig.center_window(window, AppConfig.window_width, AppConfig.window_height)

    # Make the window-non-resizable
    window.resizable(False, False)

    # Initialize the title screen
    app = WelcomeScreenApp(window)

    window.mainloop()