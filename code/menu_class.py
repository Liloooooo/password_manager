"""Module menu_class -- full menu for passwordmanager.

Decorator function sleep(function):
    Waits 4 seconds after function is executed, if and only if function does not return None
Class Menu:
    Full functionality of passwordmanager menu.
    
"""

from pw_classes import Entry, PasswordDB
from random_password import generate_random_pw
import pyperclip as pc
import re
from datetime import datetime
import time
import functools
import pickle
import difflib


def sleep(func):
    # Decorator function; sleeps 4 seconds after function is called, only if function does not return None
    @functools.wraps(func)
    def wrapper_sleep(*args, **kwargs):
        if func(*args, **kwargs):
            time.sleep(4)
        return func

    return wrapper_sleep


class Menu:
    """Menu for passwordmanager. 
    
    Attrs:
        database (PasswordDB): The database on the basis of which menu operates.

    Methods: 
        new_password(): Asks for user input and generates new password accordingly. 
        menu_choice(): Is called for full functionality of menu. 

    """

    def __init__(self, database):
        assert isinstance(database, PasswordDB)
        self.pw_db = database

    def _website_choice(self, action_string):
        # Asks for website input and lists alternative options.
        # pw_db (PasswordDB): Password database from which websites are listed.
        # action_string (String): string to be inserted into question: which website would you like to ...
        # returns entry of None if user returns to main menu
        entry = None
        print("Which website would you like to {}?".format(action_string))
        print("V: view options")
        print("M: return to menu.")
        while not entry:
            url = str(input(": "))
            if url == "V":
                self.pw_db.list_websites()
            elif url == "M":
                return None
            else:
                entry = self.pw_db.select_entry(url)
                if not entry:
                    similar = difflib.get_close_matches(
                        url, self.pw_db.list_websites(), n=1, cutoff=0
                    )[0]
                    print(
                        "No corresponding entry found. Did you mean {}?".format(
                            similar
                        )
                    )
                    print("V: view options")
                    print("M: return to menu.")
        return entry

    def _create_entry(self):
        # Creates a new Entry in PasswordDB from user inputs. Copies Entry's password to clipboard after creation.
        # pw_db (PasswordDB): Password Database to add entry to.
        new_entry_username = ""
        print("Provide website, or type M to return to menu")
        while True:
            new_entry_website = str(input(": "))
            if new_entry_website == "M":
                return None
            if bool(
                re.search(
                    "(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})",
                    new_entry_website,
                )
            ):
                break
            else:
                print("Not a valid website")
        print("Provide username or type M to return to menu")
        while len(new_entry_username.strip()) == 0:
            new_entry_username = str(input(": "))
            if new_entry_username == "M":
                return None
        new_entry_password = str(
            input("Provide the password or leave blank: ")
        )
        new_entry = Entry(new_entry_website, new_entry_username)
        if len(new_entry_password.strip()) > 0:
            new_entry.password = new_entry_password
        else:
            random_pw = input("Generate a random password? [y/n]")
            if random_pw == "y":
                new_pw = self.new_password()
                new_entry.password = new_pw
            else:
                print("No password generated.")
                pc.copy("[None]")
        self.pw_db.add_entry(new_entry)
        time.sleep(4)

    def _view_all(self):
        # Displays all entries in password database
        # pw_db (PasswordDB): password database to display entries from.
        self.pw_db.list_entries()
        time.sleep(4)

    @sleep
    def _view_entry(self):
        # Displays a specific entry in password database given a user input.
        # Copies password to clipboard.
        # pw_db (PasswordDB): Password Database to display entry from.
        # returns entry or None if user returns to main menu
        entry = self._website_choice("view")
        if entry:
            print(entry)
            if entry.password:
                pc.copy(entry.password)
                print("Password copied to clipboard.")
            else:
                pc.copy("")
        return entry

    @sleep
    def _update_entry(self):
        # Updates an entry given user input (website name, which part to update, confirmations)
        # pw_db (PasswordDB): Password Database to display entry from
        # returns entry or None if user returns to main menu
        entry = self._website_choice("update")
        if entry:
            print("\nWhat should be updated?")
            print("-" * 30)
            print("w: website")
            print("u: username")
            print("p: password")
            print("M: cancel and return to menu")
            to_update = ""
            while to_update not in ["w", "u", "p", "M"]:
                to_update = str(input(": "))
                if to_update == "w":
                    value = str(input("New website? "))
                elif to_update == "u":
                    value = str(input("New username? "))
                elif to_update == "p":
                    value = str(input("New password? "))
                elif to_update == "M":
                    return None
            entry.created_at = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            self.pw_db.update_entry(entry, to_update, value)
        return entry

    @sleep
    def _delete_entry(self):
        # Deletes a specific entry from password database given user input.
        # pw_db (PasswordDB): Password Database to delete entry from.
        # returns entry of None if user returns to main menu
        entry = self._website_choice("remove")
        if entry:
            print(
                entry, "will be removed from the database. \nContinue? [y/n]"
            )
            sure = input(": ")
            if sure == "y":
                self.pw_db.remove_entry(entry)
        return entry

    @staticmethod
    def new_password():
        """Asks for user input and generates new password accordingly. 
        
        Returns: 
            password (string): a new randomly generated password
            
        """

        print("Minimum length? Leave blank if no requirements")
        while True:
            min_length = input(": ")
            if min_length == "":
                min_length = 7
            try:
                min_length = int(min_length)
                break
            except ValueError:
                print("Minimum length must be an integer")
        print("Maximum length? Leave blank if no requirements")
        while True:
            max_length = input(": ")
            if max_length == "":
                max_length = 25
            try:
                max_length = int(max_length)
                break
            except ValueError:
                print("Maximum length must be an integer")
        while max_length < min_length:
            print(
                "Maximum length must be greater than minimum length or greater than 7 if minimum length was not specified. \nMaximum lenght"
            )
            max_length = int(input(": "))
        print("Special characters included? [y/n]")
        special = input(": ")
        special_characters = True
        if special == "n":
            special_characters = False
        print("Exlude characters? Leave blank or type characters to exclude")
        exclude = input(": ")
        exclude_list = []
        exclude_list[:0] = exclude
        random_pw = generate_random_pw(
            min_length, max_length, special_characters, exclude_list
        )
        pc.copy(random_pw)
        print("New password copied to clipboard.")
        return random_pw

    def menu_choice(self):
        """Is called for full functionality of menu."""
        choice = self._print_menu()
        while choice != "Q":
            if choice == "0":
                self._view_all()
            if choice == "1":
                self._create_entry()
                # save changes
                with open("password_db.p", "wb") as file:
                    pickle.dump(self.pw_db, file)
            if choice == "2":
                self._view_entry()
            if choice == "3":
                self._update_entry()
                # save changes
                with open("password_db.p", "wb") as file:
                    pickle.dump(self.pw_db, file)
            if choice == "4":
                self._delete_entry()
                # save_changes
                with open("password_db.p", "wb") as file:
                    pickle.dump(self.pw_db, file)
            if choice == "5":
                self.new_password()
            choice = self._print_menu()
        with open("password_db.p", "wb") as file:
            pickle.dump(self.pw_db, file)

    @staticmethod
    def _print_menu():
        # Prints password manager menu
        # returs user choice
        print("\n")
        print(("-" * 13) + "Menu" + ("-" * 13))
        print("0. View all entries")
        print("1. Create a new entry")
        print("2. View an entry and copy password")
        print("3. Update an entry")
        print("4. Delete an entry")
        print("5. Generate a random password")
        print("Q. Exit")
        print("-" * 30)
        return input(": ")
