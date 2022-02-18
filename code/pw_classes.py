"""Module pw_classes -- Classes for PasswordDB (database) and Entry (an entry in the database)

Class Entry:
    Entry in password database.
Class PasswordDB: Database class, container for Entry instances. Enables basic CRUD functionality.
    
"""

from datetime import datetime


class Entry:
    """Entry in password database.
    
    Args:
        website (str): Name of the website this entry is for.
        username (str): Username for the website.
        password (str): Password for the website. Defaults to None. 
    
    Attr:
        created_at (str): Current date and time in '%d.%m.%Y %H:%M:%S' format. Also used for updating entries. 

    """

    def __init__(self, website, username, password=None):
        assert isinstance(website, str)
        assert isinstance(username, str)
        if password:
            assert isinstance(password, str)
        self.password = password
        self.created_at = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.website = website
        self.username = username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        """Setter for password property. Checks that password is not empty string or only whitespaces."""
        if value:
            assert isinstance(value, str)
            if len(value.strip()) == 0:
                raise ValueError
        self._password = value

    @property
    def website(self):
        return self._website

    @website.setter
    def website(self, value):
        """Setter for website property. Checks that website is not empty string or only whitespaces."""
        assert isinstance(value, str)
        if len(value.strip()) == 0:
            raise ValueError
        self._website = value

    def __str__(self):
        """String representation of Entry"""
        return "{} with username {} created/updated at {}.".format(
            self.website, self.username, self.created_at
        )


class PasswordDB:
    """Database class, container for Entry instances.
    Enables basic CRUD functionality.
    
    Args:
        entries (list): List of entries. Defaults to None.
        
    """

    def __init__(self, entries=None):
        if not entries:
            entries = []
        assert isinstance(entries, list)
        if entries:
            for entry in entries:
                assert isinstance(entry, Entry)
        self.entries = entries

    def add_entry(self, item):
        """Adds entry to DB entries
        
        Args:
            item (Entry): Entry to add to entries.
            
        """

        assert isinstance(item, Entry), "item must be of class Entry"
        if (item.website in [entry.website for entry in self.entries]) and (
            item.username in [entry.username for entry in self.entries]
        ):
            print(
                "This website-username combination is already listed in the database. Use 3. update an entry to update the entry."
            )
        else:
            self.entries.append(item)
            print("Entry added to database.")

    def remove_entry(self, item):
        """Removes entry from DB entries
        
        Args:
            item (Entry): Entry to remove from entries.
            
        """

        assert isinstance(item, Entry)
        if item not in self.entries:
            raise ValueError
        self.entries.remove(item)
        print("Entry removed from database.")

    def update_entry(self, item, to_update, value):
        """Updates selected part of an entry in DB.
        
        Args:
            item (Entry): Entry to update.
            to_update (str): String defining which part of Entry to update. 
                             Must be in ('w','u','p').
            value (str): Value to use for updating.
        
        """

        assert isinstance(to_update, str)
        if to_update not in ["w", "u", "p"]:
            raise ValueError
        assert isinstance(value, str)
        if len(value.strip()) == 0:
            raise ValueError
        assert isinstance(item, Entry)
        if item not in self.entries:
            raise ValueError
        if to_update == "w":
            self.entries[self.entries.index(item)].website = value
            print("Website updated.")
        elif to_update == "u":
            self.entries[self.entries.index(item)].username = value
            print("Username updated.")
        else:
            self.entries[self.entries.index(item)].password = value
            print("Password updated.")

    def select_entry(self, website_name):
        """Searches for an Entry given a website name.
        
        Args:
            website_name (str): Website name to search entries for.
            
        Returns:
            entry (Entry): Entry with website matching website name.
                           If no matching entry is found None is returned.
                           
        """

        assert isinstance(website_name, str)
        for entry in self.entries:
            if entry.website == website_name:
                return entry

    def list_entries(self):
        """Displays all entries currently listed in database"""
        print("The following entries are saved in database:\n")
        if len(self.entries) == 0:
            print("The database is currently empty.")
        else:
            for entry in self.entries:
                print(entry)

    def list_websites(self):
        """Displays all websites currently listed in database"""
        entry_websites = [entry.website for entry in self.entries]
        for website in entry_websites:
            print(website)
        return entry_websites
