import hashlib
import sqlite3 as sql
from flask import current_app
import os

class LoginHandling():

    def __init__(self):
        pass

    def _create_connection(self) -> sql.Connection:
        try:
            db_path = current_app.config['DATABASE_PATH']
            conn = sql.connect(db_path)
            return conn
        except sql.Error as e:
            raise Exception(f"Error connecting to database: {str(e)}")
        
    def _hash_entry(self, entry):

        for i in range(0,1000):
            entry = hashlib.sha3_512(entry.encode('utf-8'))
            entry = entry.hexdigest()
        return entry

    def _check_db_exists(self, pre_check:str = '') -> bool:

        if pre_check == '':
            db_path = current_app.config['DATABASE_PATH']
        else:
            db_path = pre_check

        result = os.path.exists(db_path)

        return result
        

    def create_new_db(self, pre_check:str = '') -> bool:

        if self._check_db_exists(pre_check=pre_check) == False:

            if pre_check == '':
                db_path = current_app.config['DATABASE_PATH']
            else:
                db_path = pre_check

            conn = sql.connect(db_path)

            cursor = conn.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS User_data (
                user TEXT,
                password TEXT,
                level INTEGER
            )""")

            conn.commit()
            conn.close()

            return True
        
        else:

            return False


    def signup(self, user: str, password: str, reentry_password: str, user_level: str) -> str:

        connection = self._create_connection()
        cursor=connection.cursor()

        user = self._hash_entry(user)
        password = self._hash_entry(password)
        reentry_password = self._hash_entry(reentry_password)
        # user_level = hash_entry(user_level)

        if user != '':

            cursor.execute("SELECT count(*) FROM User_data WHERE user = ?", (user, ))
            data=cursor.fetchone()[0]

        else:

            connection.close()
            return 'No username entered'

        if data == 0:

            if reentry_password == password and password != '':
                
                cursor.execute("INSERT INTO User_data VALUES (?, ?, ?)", (user, password, user_level))
                connection.commit()

                connection.close()

                return 'Saved'

            else:

                connection.close()
                return 'Passwords do not match'

        else:

            connection.close()
            return 'User already exists'

    def write_user_level(self, user, user_level):

        user = self._hash_entry(user)
        user_level = self._hash_entry(user_level)

        update_query = """Update User_data set level = ? where user = ?"""
        data = (user_level, user)

        connection = self._create_connection()
        cursor=connection.cursor()
        cursor.execute(update_query, data)
        connection.commit()

        connection.close()

        return 'User level changed'

    def delete_user(self, user):

        user = self._hash_entry(user)    

        connection = self._create_connection()
        cursor=connection.cursor()

        cursor.execute("DELETE FROM User_data WHERE user = ?", (user, ))

        connection.commit()

        connection.close()

        return 'User deleted'

    def read_data_from_user(self, user, parameter):

        user = self._hash_entry(user)
        connection = self._create_connection()
        cursor=connection.cursor()

        cursor.execute("SELECT count(*) FROM User_data WHERE user = ?", (user, ))

        check=cursor.fetchone()[0]

        if check >= 1:

            cursor.execute("SELECT %s FROM User_data WHERE user = ?" % (parameter, ), (user, ))

            data=cursor.fetchone()[0]

            connection.close()

            return data

        else:

            return None

    def change_password(self, user, old_password, new_password, reentry_new_password):

        user = self._hash_entry(user)
        old_password = self._hash_entry(old_password)
        new_password = self._hash_entry(new_password)
        reentry_new_password = self._hash_entry(reentry_new_password)

        connection = self._create_connection()
        cursor=connection.cursor()

        cursor.execute("SELECT count(*) FROM User_data WHERE user = ?", (user, ))

        check=cursor.fetchone()[0]

        if check >= 1:

            cursor.execute("SELECT password FROM User_data WHERE user = ?", (user, ))

            password=cursor.fetchone()[0]

            if old_password == password:

                if new_password == reentry_new_password and new_password != '':

                    update_query = """Update User_data set password = ? where user = ?"""
                    data = (new_password, user)

                    cursor.execute(update_query, data)
                    connection.commit()

                    connection.close()

                    return 'Saved'

                else:

                    connection.close()
                    return 'New passwords do not match'

            else:

                connection.close()
                return 'Old password is incorrect'

        else:

            connection.close()
            return 'User does not exist'
        
    def user_login(self, user:str, password:str) -> bool:

        if self._hash_entry(password) == self.read_data_from_user(user=user, parameter='password'):

            return True
        
        else:

            return False