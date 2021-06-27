import os.path
import random
import uuid

import flask

from flask import Flask, render_template, make_response, request, redirect
import traffio.flashcard as flashcards

app = Flask(__name__, template_folder=os.path.abspath("./traffio/templates/"))

@app.route('/')
def hello():
    return '''
    Welcome to Traffio!
    <br>
    <a href="/flashcard">Start learning with flash cards</a>
    <br>
    <a href="/test">Take a test</a>
    '''

@app.route('/flashcard')
def flashcard():
    flashcard_index = random.randint(0, flashcards.get_flashcard_count())
    response = make_response(render_template("flashcard.html", flashcard_index=flashcard_index))
    return response

@app.route('/test')
def test():
    test_id = str(uuid.uuid4())
    if "TestId" in request.cookies:
        test_id = request.cookies.get("TestId")

    response = make_response(render_template("test.html", test_id=test_id))
    response.set_cookie("TestId", test_id)

    return response

@app.route('/test/end')
def test_end():
    response = make_response(redirect("/"))
    response.delete_cookie("TestId")
    return response

