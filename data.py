import sqlite3
from datetime import datetime


def get_new_id(cursor):
    highest_id = cursor.execute("SELECT MAX(id) FROM story").fetchone()[0]
    if highest_id is None:
        return None
    return str(highest_id + 1)


def read_data(cursor):
    return cursor.execute("SELECT * FROM story")


def authenticate_story(connector, cursor, id):
    raw = cursor.execute("SELECT * FROM story WHERE id=({0})".format(id))
    data = raw.fetchone()
    cursor.execute('DELETE FROM story WHERE id=({0})'.format(id))
    try:
        if data[6] == '':
            file_path = None
        else:
            file_path = data[6]
    except TypeError:
        file_path = None
    add_data_to_table(cursor, connector, data[2], data[3], data[4], file_path=file_path, approved=True,
                      unique_id=data[0], date=data[5])

    connector.commit()


def remove_story(connector, cursor, id):
    cursor.execute('DELETE FROM story WHERE id=({0})'.format(id))


def get_authorized_stories(cursor):
    return cursor.execute('SELECT * FROM story where accepted=(1)')


def get_unauthorized_stories(cursor):
    return cursor.execute('SELECT * FROM story where accepted=(0)')


def make_table(connector, cursor):
    cursor.execute('''
        CREATE TABLE story
    (
        id INTEGER PRIMARY KEY,
        accepted BOOLEAN,
        author TEXT,
        story TEXT,
        contact TEXT,
        date TEXT,
        file_path TEXT
    )
    ''')
    connector.commit()


def add_data_to_table(cursor, connector, author, story, contact, file_path=None, approved=False, unique_id=0,
                      date=str(datetime.now())):
    if not approved:
        if get_new_id(cursor) is not None:
            unique_id = get_new_id(cursor)
        else:
            unique_id = 0

    if file_path is None:
        file_path = ""

    cursor.execute('''INSERT INTO story(id, accepted, author, story, contact, date, file_path)
                      VALUES(:id, :accepted, :author, :story, :contact, :date, :file_path)''',
                   {'id': unique_id, 'accepted': approved, 'author': author,
                    'story': story, 'contact': contact, 'date': date, 'file_path': file_path})
    connector.commit()


def add_video(cursor, connector, id, video_path):

    cursor.execute('''INSERT INTO story (file_path)
                      VALUES (:file_path)
                      WHERE id=(:id)''',
                   {'file_path': video_path, 'id': id})
    connector.commit()


def build_database(connector, cursor):
    make_table(connector, cursor)
    for i in range(10):
        add_data_to_table(cursor, connector, "user1", "Story", "fakeemail@gmail.com")


def data_uri_to_file(data_uri, filepath):

    _, encoded = data_uri.split(",", 1)[1]
    data = b64decode(encoded)

    with open(filepath, "wb") as file:
        file.write(data)


if __name__ == "__main__":

    with sqlite3.connect('test.db') as connector:
        cursor = connector.cursor()

        build_database(connector, cursor)

        # authenticate_story(connector, cursor, 4)
        for row in read_data(cursor):
            print(row)
