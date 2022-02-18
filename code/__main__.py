"""Main file. If python __main__.de is called, starts password manager"""

import pickle
import hashlib
from menu_class import Menu
from pw_classes import PasswordDB
from getpass import getpass

def validate_master_pw(input_password, master_password):
    """Validates hashed input password against hashed master password.
    
    Args:
        input_password (str): Unhashed input password.
        master_password (str): Hashed master password.
    
    """

    input_password = hashlib.sha256(input_password.encode()).hexdigest()
    if input_password == master_password:
        return True
    else:
        return False


try:
    from secret import master_password
except (ModuleNotFoundError, ImportError):
    created = False
    while created == False:
        pw = getpass("Set master password: ")
        pw_hashed = hashlib.sha256(pw.encode()).hexdigest()
        with open("secret.py", "w") as file:
            file.write(f"master_password = '{pw_hashed}'")
        print("Master password set")
        created = True
        master_password = pw_hashed
access = False
tries = 2
print('+++++++++ Welcome to your password manager +++++++++')
while tries >= 0 and access == False:
    pw_given = getpass("Password: ")
    if validate_master_pw(pw_given, master_password):
        access = True
    else:
        if tries >= 1:
            print(
                "Password not correct. You have {} tries left.".format(tries)
            )
    tries -= 1
if not access:
    print("No tries left. System exits.")
if access:
    try:
        with open("password_db.p", "rb") as file:
            pw_db = pickle.load(file)
        assert isinstance(pw_db, PasswordDB)
        print("Database loaded from password_db.p")
    except FileNotFoundError:
        pw_db = PasswordDB()
        print("New database initiated")

    menu = Menu(pw_db)
    menu.menu_choice()
    exit()
