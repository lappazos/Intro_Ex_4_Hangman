##################################################################
# FILE : hangman.py
# WRITER : Lior Paz, lioraryepaz, 206240996
# EXERCISE : intro2cs ex4 2017-2018
# DESCRIPTION : hangman game - with a large scale of optional words,
# max errors of 6, and... a special option of hints!!!.
##################################################################


import hangman_helper

# allows us to use all of the helping functions that the great stuff of CS
# built for us :)


UNDERSCORE = '_'


# magic number that appear several times in my code


def update_word_pattern(word, pattern, letter):
    """The function gets a certain word, a pattern in which parts of the
    word or all of it is hidden, and a letter that is in the word. than,
    it returns us a renewed pattern in which the letter is revealed"""
    list_pattern = list(pattern)
    # im listing the pattern in order that i can change specific letters in it
    index = -1
    # im going over all of the letters in word - if a letter (or more than 1)
    #  is identical to the input letter, well change the pattern accordingly
    for l in word:
        index += 1
        if l is letter:
            list_pattern[index] = letter
    pattern = ''.join(list_pattern)
    return pattern


def filter_words_list(words_list, pattern, wrong_guess_lst):
    """This Function gets a semi-revealed pattern and aq list of wrong
    guesses, and finds all of the words that could be hidden behind the
    pattern"""
    # increase efficiency while going over the sequence
    words_set = set(words_list)
    filtered_words = []
    # we will go over every word in the index and look for matches
    for word in words_set:
        check = True
        # first we will look for length match - no match, we can skip to the
        # next word
        if len(word) != len(pattern):
            continue
        # if one of the letters in the current word were looking at was
        # already guessed - next word.
        for letter_check in word:
            if letter_check in wrong_guess_lst:
                check = False
        # in order to increase efficiency, i defined it as set so no need
        # going over double-letters - set will delete all of the repeats.
        pattern_check = set(pattern)
        for i in range(len(word)):
            # if a word has a letter we already typed in the game,
            # in a hidden spot - it is not the word we are looking for
            if (pattern[i] == UNDERSCORE) and (word[i] in pattern_check):
                check = False
            # if a un-hidden letter in the pattern is different from the
            # letter in the same spot in the check_word - not the word we need.
            if (pattern[i] != UNDERSCORE) and (pattern[i] != word[i]):
                check = False
        if not check:
            continue
        # if a word fits all of the criteria, i would include it in the
        # filtered word list
        filtered_words.append(word)
    return filtered_words


def choose_letter(filtered_words, pattern):
    """The function gives us the most common letter out of list of words. if
     there are several with the same count, it will give us the first in
      a-z """
    all_letters = ''.join(filtered_words)
    # unite the words into one large string
    max_count = (0, 0)
    # a tuple with the number of appearances and the letter
    for i in range(97, 123):
        # the range is the ord of a-z
        if chr(i) in pattern:
            continue
        else:
            current_count = all_letters.count(chr(i))
            if current_count > max_count[0]:
                # every time the largest count will win and replace max count
                max_count = (current_count, chr(i))
    return max_count


def run_single_game(words_list):
    """The function that sets the rules, laws and the center backend of the
    game itself"""
    random_word = hangman_helper.get_random_word(words_list)
    # choose the word randomly from the index
    wrong_guess_lst = set()
    pattern = UNDERSCORE * len(random_word)
    msg = hangman_helper.DEFAULT_MSG
    # mapping helper func to more comfortable variables i determined
    ask_play = False
    # i wont ask the player to play again as default, only in specific
    # Circumstances
    while (len(wrong_guess_lst) < hangman_helper.MAX_ERRORS) and (
                pattern.find(UNDERSCORE) != -1):
        error_count = len(wrong_guess_lst)
        hangman_helper.display_state(pattern, error_count, wrong_guess_lst,
                                     msg, ask_play)
        # the main function that sends data to the player, the "game" itself
        key, value = hangman_helper.get_input()
        if key == hangman_helper.HINT:
            filtered_words = filter_words_list(words_list, pattern,
                                               wrong_guess_lst)
            hint = (choose_letter(filtered_words, pattern))[1]
            msg = hangman_helper.HINT_MSG + hint
            continue
        # every time we understand what has the player asked for, there is no
        # need to check all of the other options, that's why we will continue
        elif key == hangman_helper.LETTER:
            letter_now = str(value)
            if (len(letter_now) != 1) or ((ord(letter_now) < 97) or (ord(
                    letter_now) > 122)):
                # checks if the input is a valid letter
                msg = hangman_helper.NON_VALID_MSG
            elif pattern.find(letter_now) != (-1):
                # checks if we have already chosen the letter before hand
                msg = hangman_helper.ALREADY_CHOSEN_MSG + letter_now
                continue
            elif letter_now in wrong_guess_lst:
                msg = hangman_helper.ALREADY_CHOSEN_MSG + letter_now
                continue
            elif random_word.find(letter_now) == (-1):
                # sets what happens to wrong guess
                wrong_guess_lst.add(letter_now)
                msg = hangman_helper.DEFAULT_MSG
                continue
            else:
                # the proper game where the pattern updates
                pattern = update_word_pattern(str(random_word), pattern,
                                              letter_now)
                msg = hangman_helper.DEFAULT_MSG
    if len(wrong_guess_lst) == hangman_helper.MAX_ERRORS:
        # ending the game if we have reached max errors and asks
        #  the player to play again while showing him loss msg
        msg = hangman_helper.LOSS_MSG + random_word
        error_count = hangman_helper.MAX_ERRORS
        ask_play = True
    if pattern.find(UNDERSCORE) == -1:
        # if the world is revealed - win! msg + end game
        msg = hangman_helper.WIN_MSG
        ask_play = True
    hangman_helper.display_state(pattern, error_count, wrong_guess_lst, msg,
                                 ask_play)


def main():
    """The spine of hangman - start single game im the first time and every
    time the player asks to play again"""
    # load the word index
    words_list = hangman_helper.load_words('words.txt')
    run_single_game(words_list)
    key, value = hangman_helper.get_input()
    # evaluates whether or not to play again
    if key == hangman_helper.PLAY_AGAIN:
        while value:
            run_single_game(words_list)
            key, value = hangman_helper.get_input()


if __name__ == "__main__":
    # starts the hangman.helper game
    hangman_helper.start_gui_and_call_main(main)
    hangman_helper.close_gui()