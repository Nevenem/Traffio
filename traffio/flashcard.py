import traffio.db as db


class Flashcard:
    def __init__(self, idx, name, description):
        self.idx = idx
        self.name = name
        self.description = description


def get_flashcard_index_range():
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("select count(*) from flashcard;")
    row = cur.fetchone()
    return (1, row[0])


def get_flashcard(index):
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("select * from flashcard where id=?;", (index,))
    idx, name, description = cur.fetchone()
    return Flashcard(idx, name, description)
