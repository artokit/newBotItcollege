import sqlite3
from sqlite3 import IntegrityError


def add_sender(user_id):
    connect = sqlite3.connect('sender.sqlite')
    cursor = connect.cursor()

    try:
        cursor.execute("INSERT INTO SENDER_IDS VALUES(?)", (user_id, ))
        connect.commit()

    except IntegrityError:
        pass

    cursor.close()
    connect.close()
