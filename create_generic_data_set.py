from sqltests import *

with sqlite3.connect('test.db') as connector:
    cursor = connector.cursor()

    build_database(connector, cursor)
    for i in range(10):
        add_data_to_table(cursor, connector, 'user '+str(i), 'storyData', '444-4444')
