# Problem Set 2, hangman.py
# Name: Alina
# Collaborators:
# Time spent: one month

# Hangman Game


import random
import string

START_WARN = 3
START_ATTEMPTS = 6
WORDLIST_FILENAME = "words.txt"
GAP = "_"
STAR = "*"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    """
    print("Loading word list from file...")

    inFile = open(WORDLIST_FILENAME, 'r')

    line = inFile.readline()

    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


wordlist = load_words()
secret_word = choose_word(wordlist)


def is_word_guessed(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing; assumes all letters are
        lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
        assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
        False otherwise
    """
    set_secret_word = set(secret_word)
    if (set_secret_word & letters_guessed) == set_secret_word:
        return True
    else:
        return False


def get_guessed_word(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
        which letters in secret_word have been guessed so far.
    """
    # the name changes 'replacement' indicates that it replaces an unpredictable letter
    replacement = (''.join(["_ " if not i in letters_guessed else i for i in secret_word])).rstrip()
    return replacement


def get_available_letters(letters_guessed):
    """
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
        yet been guessed.
    """
    values_values = (''.join(["" if i in letters_guessed else i for i in string.ascii_lowercase]))
    return values_values


def start(secret_word, warn):
    """
    secret_word: string, the word the user is guessing
    returns: string, greeting line, indicates the length of the word.
    """
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", len(secret_word), "letters long.")
    print('You have', warn, 'warnings left.')


def condition(attempt, letters_guessed):
    """
    attempts: number of available attempts
    letters_guessed: list (of letters), which letters have been guessed so far.
    returns: how many attempts the player has left and a list of letters that have not been used
    """
    print(20 * '-')
    print('You have', attempt, 'guesses left.')
    print('Available letters:', get_available_letters(letters_guessed))


def match_with_gaps(my_word, other_word):
    """
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    """
    if len(my_word) == len(other_word):
        for i in range(len(my_word)):
            if my_word[i] != GAP and my_word[i] != other_word[i]:
                return False
            elif my_word[i] == GAP and other_word[i] in my_word:
                return False
        return True
    else:
        return False


def show_possible_matches(my_word):
    """
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
        Keep in mind that in hangman when a letter is guessed, all the positions
        at which that letter occurs in the secret word are revealed.
        Therefore, the hidden letter(_ ) cannot be one of the letters in the word
        that has already been revealed.
    """
    lst = []
    my_word = my_word.replace(" ", "")
    for other_word in wordlist:
        if match_with_gaps(my_word, other_word):
            lst.append(other_word)
    print('Possible word matches are:', ' '.join(lst))
    if not lst:
        print("No matches found.")


def error(letters_guessed, letter, attempt, warn):
    """
    letters_guessed: list (of letters), which letters have been guessed so far.
    letter: a character that the user enters when guessing words.
    attempt: number of player attempts.
    warn: the number of player warnings for the game.
    The function checks if the player has guessed the letter. If not, it takes attempts
    returns: the number of attempts and warnings left by the player
        and provides a condition in certain cases, returns the set of letters that were used.
    """

    if letter in letters_guessed:
        # checks if the user has re-entered the letter
        if warn <= 0:
            attempt -= 1
            print("Oops! You've already guessed that letter. You have no warnings left so you lose one guess:",
                  get_guessed_word(secret_word, letters_guessed))

        else:
            warn -= 1
            print("Oops! You've already guessed that letter. You have", warn, " warnings left:",
                  get_guessed_word(secret_word, letters_guessed))

    else:
        letters_guessed.add(letter)
        # checks if the user has guessed the letter
        if letter in secret_word:
            print('Good guess:', get_guessed_word(secret_word, letters_guessed))
        # checks that the letter was not guessed
        else:
            if letter in "aeoui":
                attempt -= 2
            else:
                attempt -= 1
            print('Oops! That letter is not in my word:', get_guessed_word(secret_word, letters_guessed))

    return letters_guessed, attempt, warn


def error_input(warn, attempt, letters_guessed):
    """
    letters_guessed: list (of letters), which letters have been guessed so far.
    attempt: number of player attempts.
    warn: the number of player warnings for the game.
    returns: the number of attempts and warnings left by the player
        and provides a condition in certain cases.
    """

    if warn >= 1:
        warn -= 1
        print('Oops! That is not a valid letter. You have', warn, ' warnings left:',
              get_guessed_word(secret_word, letters_guessed))
    else:
        attempt -= 1
        print("Oops!  That is not a valid letter. You have no warnings left so you lose one guess:",
              get_guessed_word(secret_word, letters_guessed))
    return warn, attempt


def hangman(secret_word, hints=False):
    """
    secret_word: string, the secret word to guess.
    Starts up an interactive game of Hangman.
    """
    letters_guessed = set()
    attempt = START_ATTEMPTS
    warn = START_WARN
    start(secret_word, warn)

    while attempt > 0:
        condition(attempt, letters_guessed)
        letter = input('Please guess a letter:').lower()
        # checks if the user wants to play with hints
        if hints and letter == STAR:
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            continue
        # checks if the user has entered the data correctly
        elif not letter.isalpha() or len(letter) != 1 or not letter.isascii():

            warn, attempt = error_input(warn, attempt, letters_guessed)
        # checks if the user has guessed the letter
        else:
            letters_guessed, attempt, warn = error(letters_guessed, letter, attempt, warn)
        # checks if the user has guessed the word
        if is_word_guessed(secret_word, letters_guessed):
            print(20 * '-')
            print('Congratulations, you won! Your total score for this game is:',
                  attempt * len(set(secret_word)))
            break
    else:
        print('Sorry, you ran out of guesses. The word was', secret_word)


def hangman_with_hints(secret_word):
    """
    secret_word: string, the secret word to guess.
    Starts up an interactive game of Hangman.
    """
    hangman(secret_word, True)


if __name__ == "__main__":

    # To play the game 'Gallows' without prompts, comment out 215 - 217 lines of code

    # To play the game 'Hangman' with hints uncomment 215 - 217 lines of code !

    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
