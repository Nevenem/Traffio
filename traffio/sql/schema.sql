DROP TABLE IF EXISTS flashcard;
DROP TABLE IF EXISTS test;

CREATE TABLE flashcard (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  description TEXT NOT NULL
);

CREATE TABLE test (
    id VARCHAR PRIMARY KEY,
    currentQuestion INTEGER NOT NULL,
    questionCount INTEGER NOT NULL,
    correctCount INTEGER NOT NULL,
    answer1 INTEGER NOT NULL,
    answer2 INTEGER NOT NULL,
    answer3 INTEGER NOT NULL,
    answer4 INTEGER NOT NULL,
    correctAnswer INTEGER NOT NULL,
    FOREIGN KEY(answer1) REFERENCES flashcard(id),
    FOREIGN KEY(answer2) REFERENCES flashcard(id),
    FOREIGN KEY(answer3) REFERENCES flashcard(id),
    FOREIGN KEY(answer4) REFERENCES flashcard(id),
    FOREIGN KEY(correctAnswer) REFERENCES flashcard(id)
);
