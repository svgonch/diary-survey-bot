import sqlite3
import pickle
import time

INIT, SET = range(2)


class User:
    participants = {}

    def __init__(self):
        return

    def get_participant(self, chat_id):
        return self.participants[chat_id]

    def add_participant(self, user):
        self.participants[user.chat_id] = user
        return


class Participant:
    chat_id_ = None
    language_ = None
    gender_ = None
    country_ = None
    day_ = 0
    time_t_ = None
    time_offset_ = 0
    conditions_ = []

    state = INIT
    q_current_ = -1
    q_idle_ = False

    def __init__(self, chat_id=None):
        self.chat_id_ = chat_id
        db = sqlite3.connect('user/participants.db')
        db.execute("INSERT INTO participants (ID, conditions, time_offset, time_t, day_t, country, gender, language) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (chat_id, None, 0, '', 0, '', '', ''))
        db.commit()
        db.close()
        text = "User: " + str(self.chat_id_) + " registered. " + time.strftime("%X %x\n")
        with open('log.txt', 'a') as log:
            log.write(text)

    def set_language(self, language):
        self.language_ = language
        db = sqlite3.connect('participants.db')
        db.execute("UPDATE participants SET language=? WHERE ID=?", (language, self.chat_id_))
        db.commit()
        db.close()
        return

    def set_gender(self, gender):
        self.gender_ = gender
        db = sqlite3.connect('participants.db')
        db.execute("UPDATE participants SET gender=? WHERE ID=?", (gender, self.chat_id_))
        db.commit()
        db.close()
        return

    def set_country(self, country):
        self.country_ = country
        db = sqlite3.connect('participants.db')
        db.execute("UPDATE participants SET country=? WHERE ID=?", (country, self.chat_id_))
        db.commit()
        db.close()
        return

    def increase_day_t(self):
        self.day_ += 1
        db = sqlite3.connect('user/participants.db')
        db.execute("UPDATE participants SET day_t=? WHERE ID=?", (self.day_, self.chat_id_))
        db.commit()
        db.close()
        return self.day_

    def set_time_t(self, time):
        self.time_t_ = time
        db = sqlite3.connect('user/participants.db')
        db.execute("UPDATE participants SET time_t=? WHERE ID=?", (time, self.chat_id_))
        db.commit()
        db.close()
        return

    def set_time_offset(self, offset):
        self.time_offset_ = offset
        db = sqlite3.connect('user/participants.db')
        db.execute("UPDATE participants SET time_offset=? WHERE ID=?", (offset, self.chat_id_))
        db.commit()
        db.close()
        return

    def set_conditions(self, conditions):
        self.conditions_ += conditions
        db = sqlite3.connect('user/participants.db')
        cursor = db.cursor()
        cursor.execute("SELECT conditions FROM participants WHERE ID=?", self.chat_id_)
        fetch = cursor.fetchone()  # type: list
        cond_blob = fetch[0]  # type: pickle
        cond_old = pickle.loads(cond_blob)
        cond = pickle.dumps(cond_old + conditions)
        db.execute("UPDATE participants SET conditions=? WHERE ID=?", (cond, self.chat_id_))
        db.commit()
        db.close()
        return

    def delete_participant(self):
        db = sqlite3.connect('user/participants.db')
        db.execute("DELETE FROM participants WHERE ID=?", (self.chat_id_,))
        db.commit()
        db.close()
        print('deleted' + str(self.chat_id_))
        return 0


def initialize_participants():
    db = sqlite3.connect('user/participants.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM participants ORDER BY (ID)")
    participants = cursor.fetchall()
    # TODO


def clean_database():
    return
    # Todo

















