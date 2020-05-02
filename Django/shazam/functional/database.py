import psycopg2
import json
import os
from shazam.functional.fingerprint import create_fingerprint


def fill_db(db_connection, path_to_base):
    tracks = os.listdir(path_to_base)
    index = {}
    id_names = {}
    for idx, file in enumerate(tracks):
        if file.endswith('.mp3') or file.endswith('.wav'):
            print(idx, 'of', len(tracks))
            id_names.update({idx: file})
            index, _ = create_fingerprint(os.path.join(path_to_base, file), idx, index)
    cursor = db_connection.cursor()

    postgres_insert_song_query = 'INSERT INTO shazam_song (id, name, author) VALUES (%s,%s, %s)'

    postgres_insert_fingerprint_query = 'INSERT INTO shazam_fingerprint ' \
                                        '(hash_value, song_id_id, time_stamp) VALUES (%s,%s,%s)'
    for i in id_names:
        song = (i, id_names[i], '')
        cursor.execute(postgres_insert_song_query, song)
        db_connection.commit()

    for i in index:
        for j in range(len(index[i])):
            fingerprint = (i, int(index[i][j][1]), int(index[i][j][0]))
            cursor.execute(postgres_insert_fingerprint_query, fingerprint)
    db_connection.commit()


if __name__ == '__main__':

    try:
        filename = 'db_creds.json'
        # ToDo Parsing from command line arguments
        with open(filename) as rf:
            creds = json.load(rf)

    except FileNotFoundError:
        print('Credentials of database not found')
        exit(1)
    try:

        connection = psycopg2.connect(user=creds['user'],
                                      password=creds['password'],
                                      host=creds['host'],
                                      port=creds['port'],
                                      database=creds['database'])
        try:
            fill_db(connection, '../../../audio_database/')
        except (Exception, psycopg2.Error) as error:
            print('Some shit happened, because you are stupid idiot!')
    except (Exception, psycopg2.Error) as error:
        if (connection):
            print("Failed to insert record into mobile table", error)

    finally:
        # closing database connection.
        if (connection):
            connection.close()
            print("PostgreSQL connection is closed")
