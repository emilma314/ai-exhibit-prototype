import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import string
from collections import Counter
import re
import string

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index():
    return render_template('exhibit1.html')

@app.route('/match/<difficulty>')
def match(difficulty):
    return render_template('match.html', difficulty=difficulty)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/exhibit2')
def exhibit2():
    return render_template('exhibit2.html')

@app.route('/denoise')
def denoise():
    pair = request.args.get('pair')

    if pair == 'pair1':
        code_snippet = "print('Hello from Pair 1!')"
    elif pair == 'pair2':
        code_snippet = "print('Hello from Pair 2!')"
    elif pair == 'pair3':
        code_snippet = "print('Hello from Pair 3!')"
    elif pair == 'pair4':
        code_snippet = "print('Hello from Pair 4!')"
    else:
        code_snippet = "Invalid selection."

    return render_template('denoise.html', code_snippet=code_snippet)



@app.route('/occurrences.html')
def occurrences():
    word = request.args.get('word')
    occurrences = find_occurrences(word)  # Implement this function to find occurrences
    return render_template('occurrences.html', word=word, occurrences=occurrences[:10])
def alit():
    with open('moby.txt', 'r') as f:
        text = f.read()

    sentences = re.split(r'(?<=[.!?]) +', text)
    alit = []
    bad = ['the', 'to', 'of', 'on', 'that', 'then', 'at', 'a', 'an', 'they', 'such', 'it', 'in']
    chapter = 0

    for i in range(1, len(sentences) - 1):
        sentence = sentences[i]
        words = re.findall(r'\b\w+\b', sentence)
        non_trivial_words = [word for word in words if len(word) > 3]

        for j in range(len(non_trivial_words) - 2):
            word_a = non_trivial_words[j]
            word_b = non_trivial_words[j + 1]
            word_c = non_trivial_words[j + 2]

            if word_b.lower() == 'chapter':
                chapter += 1

            if word_a[0].lower() == word_b[0].lower() == word_c[0].lower():
                if not any(x in bad for x in (word_a.lower(), word_b.lower(), word_c.lower())):
                    context = sentences[i - 1] + " " + sentences[i] + " " + sentences[i + 1]
                    alit.append(("chapter: {}".format(chapter), word_a, word_b, word_c, context))
    return alit

def find_3_word_alliterations():
    with open("moby.txt", 'r') as file:
        text = file.read().lower()

    chapters = re.split(r'CHAPTER (?=\d+)', text)
    alliterations = []

    for chapter_num, chapter in enumerate(chapters, start=1):
        sentences = re.split(r'(?<=[.!?]) +', chapter)
        for sentence in sentences:
            words = re.findall(r'\b\w+\b', sentence)
            non_trivial_words = [word for word in words if len(word) > 3]

            for i in range(len(non_trivial_words) - 2):
                window = non_trivial_words[i:i + 3]
                first_letters = [word[0] for word in window]
                if len(set(first_letters)) == 1:
                    alliterations.append((chapter_num, sentence, [w.lower() for w in window]))

    return alliterations


@app.route('/alliterations')
def display_alliterations():
    alliterations = alit()
    #limited_alliterations = alliterations[:200]  # Limit to first 10 results
    return render_template('alliterations.html', alliterations=alliterations)

def find_occurrences(word):
    occurrences = []
    with open("moby.txt", "r") as f:
        f = f.read()
        sentences = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', f)
        for index,sentence in enumerate(sentences):
            if word in sentence.lower().translate(str.maketrans('', '', string.punctuation)).split():
                occurrences.append(" ".join(sentences[index-1:index+2]))
            if len(occurrences) == 10:
                break
    return occurrences
