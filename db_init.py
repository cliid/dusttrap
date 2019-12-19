import sqlite3

user_id_db_location = './databases/user.db'
print('INIT DATABASE Called...')
try:
    # INIT user_id db...
    conn = sqlite3.connect(user_id_db_location)
    c = conn.cursor()

    c.execute(
        "CREATE TABLE user ("
        "user_id text, "
        "title text, "
        "suggestions text )"
    )

    conn.commit()
    conn.close()
except sqlite3.OperationalError:
    print('DB Init failed...')