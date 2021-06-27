import random

import traffio.flashcard
from traffio.db import get_db


class Test:
    def __init__(self, test_id, question_count, num_flashcards):
        self.test_id = test_id
        self.question_count = question_count
        self.num_flashcards = num_flashcards
        self.correct_count = 0
        self.current_question = 1
        self.answers = ()
        self.correct_answer = -1

        # Initialize the first question
        self.next_answer()

    def next_answer(self):
        self.answers = (
            random.randint(1, self.num_flashcards),
            random.randint(1, self.num_flashcards),
            random.randint(1, self.num_flashcards),
            random.randint(1, self.num_flashcards),
        )
        self.correct_answer = self.answers[random.randint(0, 3)]

    def answer_question(self, choice):
        if self.answers[choice] == self.correct_answer:
            self.correct_count += 1

        self.current_question += 1
        print(self.current_question)
        self.next_answer()
        store_test(self)

    def set_answer(self, answers, correct_answer):
        self.answers = answers
        self.correct_answer = correct_answer

    def is_complete(self):
        return self.current_question == self.question_count


def create_test(test_id, question_count=3):
    return Test(
        test_id, question_count, traffio.flashcard.get_flashcard_index_range()[1]
    )


def store_new_test(test):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        f"""
            INSERT INTO test 
            VALUES
                (
                ?, ?, ?, ?, ?, ?, ?, ?, ?
                );
        """,
        (
            test.test_id,
            test.current_question,
            test.question_count,
            test.correct_count,
            test.answers[0],
            test.answers[1],
            test.answers[2],
            test.answers[3],
            test.correct_answer,
        ),
    )
    conn.commit()


def store_test(test):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        f"""
            UPDATE test
            SET
                currentQuestion = ?,
                correctCount = ?,
                answer1 = ?,
                answer2 = ?,
                answer3 = ?,
                answer4 = ?,
                correctAnswer = ?
            WHERE id = ?
        """,
        (
            test.current_question,
            test.correct_count,
            test.answers[0],
            test.answers[1],
            test.answers[2],
            test.answers[3],
            test.correct_answer,
            test.test_id,
        ),
    )
    conn.commit()


def get_test(test_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT * FROM test
        WHERE id = ?
    """,
        (test_id,),
    )
    row = cur.fetchone()
    (
        test_id,
        current_question,
        question_count,
        correct_count,
        a1,
        a2,
        a3,
        a4,
        correct_answer,
    ) = row

    current_test = Test(
        test_id, question_count, traffio.flashcard.get_flashcard_index_range()[1]
    )
    current_test.current_question = current_question
    current_test.correct_count = correct_count
    current_test.set_answer((a1, a2, a3, a4), correct_answer)

    return current_test
