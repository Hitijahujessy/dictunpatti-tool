""" Dictionary Unpatti Tool

A CLI tool used for searching through Universitas Pattimura's Ambonese - English dictionary.

Current features:
    - Save the dictionary in a .csv file
    - Search function
    - Jumping to page
    - Next/previous page on key press
    - Go back to page after using search function
    - Reload the dictionary (if .csv file has been lost/corrupted)

Planned features:
    - Save specific dictionary entries to personal list/favorites
    - Show random dictionary entry on main menu

"""

import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
from time import sleep
import progressbar
import os
import keyboard


class MainApp:
    df = pd.DataFrame()
    view = False

    default = '\033[0m'
    red = "\033[0;31m"
    green = "\033[0;32m"
    yellow = "\033[0;33m"
    white = "\033[0;37m"
    bold = '\033[1m'

    def create_df(self):
        """This function downloads the dictionary and saves it as dict.csv
    """
        os.system('cls')

        i = 1
        n = 127

        print("The dictionary will now be downloaded. This could take a few minutes.\nDon't close this application.\nYou are free to use your device "
              f"during this process.\n{self.green}")
        sleep(.5)
        bar = progressbar.ProgressBar(maxval=n,
                                      widgets=[progressbar.Bar('=', '[', ']'), ' ',
                                               progressbar.Percentage()])
        bar.start()
        df = []
        for x in range(n):

            url = f'https://dict.unpatti.ac.id/?page=%d' % i
            table = pd.DataFrame(pd.read_html(url)[1])
            table.drop(table.tail(6).index,
                         inplace=True)
            table.dropna(inplace=True)
            df.append(table)


            i += 1
            bar.update(x + 1)
            #sleep(0.1)

        df = pd.concat(df)
        df.to_csv('dict.csv', index=False)
        bar.finish()
        input(f"{self.default}Dictionary is ready to use! Press {self.green}enter{self.default} to go to the main menu.")
        sleep(2)
        self.menu()

    def menu(self):
        """This function shows a simple menu

        """

        title = "Unpatti Dictionary Tool - Explore Unpatti's Dictionary from your console."

        menu_options = {
            1: "View Dictionary",
            2: "Custom Lists",
            3: "Reload Dictionary",
            4: "Exit"
        }

        def print_menu():
            print("###########")
            for key in menu_options.keys():
                print("#", key, "--", menu_options[key])
            print("###########")

        # Clearing the Screen
        os.system('cls')
        print(title)
        sleep(.25)
        print_menu()
        option = input(">> ")
        if option == "1":
            self.view = True
            self.view_dictionary()
        if option == "3":
            os.system('cls')
            print(f"{self.red}{self.bold}WARNING!{self.default}\n"
                  f"{self.red}You chose to reload the dictionary. Doing this will take a few minutes and closing the "
                  "program\nduring this process will cause the dictionary to be incomplete. This is only recommended "
                  "if the\ndictionary was not downloaded correctly.\n")
            sleep(2)
            certain = input(f"Are you sure you want to reload the dictionary? (y/n){self.default}\n>>").lower()
            if certain == "y":
                self.create_df()
            else:
                self.menu()
        elif option == "4":
            quit()

    def view_dictionary(self):
        """This function prints dictionary pages

        Each page contains 30 words. The user is able to switch pages
        using the arrow keys, or by typing 'goto [page number]'.
        
        """
        df = pd.read_csv("dict.csv")

        page_start = 0
        page_end = 30
        page = df[page_start:page_end]

        

        while self.view:
            os.system('cls')
            print(f"{page_start}\n{page_end}")
            with pd.option_context('display.max_rows', None,
                                   'display.max_columns', None,
                                   'display.precision', 100, ):
                print(page)

            print(f"\nUse the {self.green}<arrow keys>{self.default} to go to the next or previous page.")
            print(f"Press {self.green}<P>{self.default} to jump to a specific page.")
            print(f"Press {self.green}<S>{self.default} to search for a specific word.")
            print(f"Press {self.green}<Q>{self.default} to go back to the menu.")

            while True:
                if keyboard.is_pressed('q'):
                    sleep(.25)
                    self.view = False
                    self.menu()
                    break
                elif keyboard.is_pressed('right_arrow'):
                    sleep(.25)
                    page_start += 30
                    page_end += 30
                    page = df[page_start:page_end]
                    break
                    # print('test', page)
                elif keyboard.is_pressed('left_arrow'):
                    sleep(.25)
                    if page_start >= 30:
                        page_start -= 30
                        page_end -= 30
                        page = df[page_start:page_end]
                        break
                    else:
                        continue
                elif keyboard.is_pressed('p'):
                    sleep(.25)
                    print(f"Type the page number ({self.green}1-128{self.default})")
                    try:
                        num = input(">>")
                    except Exception as e:
                        print(e)
                    if int(num) <= 128:
                        page_start = int(num) * 30 - 30
                        page_end = page_start + 30
                        page = df[page_start:page_end]
                        break
                elif keyboard.is_pressed('s'):
                    sleep(.25)
                    print(f"You may search for both Ambonese and English entries.\n{self.green}Search{self.default}:")
                    search_string = input(">>")

                    while True:
                        result = df[df.apply(lambda row: search_string in row.to_string(), axis=1)]
                        print(result)
                        print(f"\n{self.green}Search{self.default}, or {self.green}press enter{self.default} to go back to the dictionary:")
                        search_string = input(">>")
                        if search_string != "":
                            continue
                        else:
                            break
                    break
        

app = MainApp()

if __name__ == "__main__":
    # Download the dictionary if it doesn't exists.
    if not os.path.exists("dict.csv"):
        app.create_df()

    app.menu()
