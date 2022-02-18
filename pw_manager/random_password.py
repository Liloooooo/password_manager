"""Module random_password -- functions for random password generation.

Function load_pw_components(filepath, col): 
    Loads lists of English and German words as well as punctuation for password generation.
Function generate_random_pw(min_length, max_length, special_characters, exclude_characters): 
    Generates random password string from given parameters and components_dict.

"""

from string import punctuation
import csv
import re
import random


def load_pw_components(filepath="eng_words.csv", col=1):
    """Loads lists of English and German words as well as punctuation for password generation.
    
    Args:
        filepath (str): Path to csv or json file with english words. Defaults to 'eng_words.csv'. 
        col (int): If csv file, indicate column with words. Defaults to 1.
    Returns:
        components_dict (dict): Dict with keys = ['special_characters', 'eng_words']
                                and their corresponding lists as values.
                                
    """

    assert isinstance(filepath, str)
    is_csv = bool(re.search(".csv$", filepath))
    is_json = bool(re.search(".csv$", filepath))
    assert is_csv or is_json
    components = {}
    punct = [str(s) for s in punctuation]
    if is_csv:
        with open(filepath, "r") as csv_file:
            reader = csv.reader(csv_file)
            eng_words = [entry[col] for entry in list(reader)]
    else:
        with open(filepath) as json_file:
            eng_words = json.load(json_file)
    components["eng_words"] = eng_words
    components["special_characters"] = punct
    return components


def generate_random_pw(
    min_length=7,
    max_length=25,
    special_characters=True,
    exclude_characters=None,
):
    """Generates random password string from given parameters and components_dict.
    
    Args:
        min_length (int): Minimum character length of generated password. Defaults to 7.
        max_length (int): Maximum character length of generated password. Defaults to 25.
        special_characters (bool): Whether to include special characters. Defaults to True.
        exclude_characters (list): List of characters to exclude from password generation.
                                   Defaults to None.
    
    Returns:
        password (str): Randomly generated password string containing letters, 
                        integers and special characters (unless excluded).
    
    """

    search_dict = load_pw_components()
    while True:
        words = []
        words.append(str(random.randrange(0, 10)))
        words.append(random.choice(search_dict["eng_words"]))
        if special_characters:
            words.append(random.choice(search_dict["special_characters"]))
        random.shuffle(words)
        random_pw = "".join(words)
        if len(random_pw) >= min_length and len(random_pw) <= max_length:
            if not exclude_characters:
                return random_pw
            else:
                assert isinstance(exclude_characters, list)
                not_allowed = [
                    entry for entry in exclude_characters if entry in random_pw
                ]
                if not not_allowed:
                    return random_pw
