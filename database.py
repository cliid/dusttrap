import sqlite3


class DataBase:
    user_id_db_location = './databases/user.db'

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