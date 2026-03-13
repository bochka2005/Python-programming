def mask_word(word, guessed):
    result = ""
    for letter in word:
        if letter in guessed:
            result += letter
        else:
            result += "■"
    return result

def choose_lives(level):
    if level == 1:
        return 7
    elif level == 2:
        return 5
    elif level == 3:
        return 3
    else:
        return 5
