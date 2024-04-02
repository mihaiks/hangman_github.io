from flask import Flask, request, render_template
import random
from words import word_list

app = Flask(__name__)

word = ""
guessed_letters = []
wrong_guesses = 0

def update_word_display():
    display = ""
    for char in word:
        if char in guessed_letters:
            display += char
        else:
            display += "_"
        display += " "
    return display

@app.route('/')
def hangman():
    global word
    global guessed_letters
    global wrong_guesses
    word = random.choice(word_list)
    guessed_letters = []
    wrong_guesses = 0
    word_display = update_word_display()
    return render_template('index.html', word_display=word_display, guessed_letters=guessed_letters, wrong_guesses=wrong_guesses)

@app.route('/guess', methods=['POST'])
def guess():
    global guessed_letters
    global wrong_guesses
    letter = request.form['letter']
    guessed_letters.append(letter)
    if letter not in word:
        wrong_guesses += 1
    word_display = update_word_display()
    if all(char in guessed_letters for char in word) and guessed_letters:
        message = "Congratulations! You've guessed the word: '{}'".format(word)
    elif wrong_guesses == 6:
        message = "Game Over! The word was: '{}'".format(word)
    else:
        message = ""
    return render_template('index.html', word_display=word_display, guessed_letters=guessed_letters, wrong_guesses=wrong_guesses, message=message)

if __name__ == '__main__':
    app.run(debug=True)
