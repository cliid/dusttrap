import sqlite3


class DataBase:
    user_id_db_location = './databases/user.db'

    def init_database(self):
        print('INIT DATABASE Called...')
        try:
            # INIT user_id db...
            conn = sqlite3.connect(self.user_id_db_location)
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
            print('USER ID DB Init failed...')

    def create_user(self, user_id, title, suggestions):
        conn = sqlite3.connect(self.user_id_db_location)
        c = conn.cursor()

        c.execute(
            "INSERT INTO user VALUES ('%s', '%s', '%s')" % (user_id, title, suggestions))
        conn.commit()
        conn.close()

        return {
            "result": "success"
        }