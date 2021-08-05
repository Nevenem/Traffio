from flask import (
    Flask,
    render_template,
    make_response,
    request,
    redirect,
    send_from_directory,
)
import traffio.flashcard as flashcards
import os, random, uuid

import traffio.test


def create_app(test_config=None):
    app = Flask(__name__, template_folder=os.path.abspath("./traffio/templates/"))

    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "traffio.sqlite"),
    )

    if test_config:
        app.config.from_mapping(test_config)

    @app.route("/")
    def hello():

        response = make_response(render_template("index.html"))
        return response
        # return """
        # Welcome to Traffio!
        # <br>
        # <a href="/flashcard">Start learning with flash cards</a>
        # <br>
        # <a href="/test">Take a test</a>
        # """

    @app.route("/flashcard")
    def flashcard():
        min_idx, max_idx = flashcards.get_flashcard_index_range()
        flashcard_index = random.randint(min_idx, max_idx)
        fc = flashcards.get_flashcard(flashcard_index)

        response = make_response(render_template("flashcard.html", flashcard=fc))
        return response

    @app.route("/test")
    def test():
        test_id = str(uuid.uuid4())
        if "TestId" in request.cookies:
            test_id = request.cookies.get("TestId")
            current_test = traffio.test.get_test(test_id)
        else:
            current_test = traffio.test.create_test(test_id)
            traffio.test.store_new_test(current_test)

        answers = (
            flashcards.get_flashcard(current_test.answers[0]),
            flashcards.get_flashcard(current_test.answers[1]),
            flashcards.get_flashcard(current_test.answers[2]),
            flashcards.get_flashcard(current_test.answers[3]),
        )
        response = make_response(
            render_template("test.html", test=current_test, answers=answers)
        )
        response.set_cookie("TestId", test_id)

        return response

    @app.route("/test/answer", methods=["POST"])
    def answer_test():
        print(request.form)
        answer_id = request.form["answers"]

        test_id = request.cookies.get("TestId")
        current_test = traffio.test.get_test(test_id)

        current_test.answer_question(int(answer_id))
        response = make_response(redirect("/test"))
        return response

    @app.route("/sign_img/<path:path>")
    def sign_img(path):
        return send_from_directory("media", path)

    @app.route("/test/end")
    def test_end():
        response = make_response(redirect("/"))
        response.delete_cookie("TestId")
        return response

    from . import db

    db.init_app(app)

    return app
