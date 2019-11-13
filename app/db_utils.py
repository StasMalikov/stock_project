import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

class DbUtils:

    def insert_user(login, password, email, user_type, full_name):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        password_hash = generate_password_hash(password)
        cursor.execute("insert into USERS(LOGIN, PASSWORD, EMAIL, USER_TYPE, FULL_NAME) values(?,?,?,?,?)", (login, password_hash, email, user_type, full_name))
        conn.commit()
        
    def select_test():
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute('''SELECT Name FROM TEST''')
        result = cursor.fetchone()
        print(result[0])
        return result[0]


    def select_users():
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute('''SELECT LOGIN, EMAIL, USER_TYPE, FULL_NAME FROM USERS''')
        return cursor.fetchall()

    def get_user_password(login):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("SELECT PASSWORD FROM USERS WHERE LOGIN = '" + login +"';")
        result = cursor.fetchone()
        if result is not None:
                return result[0]
        else:
            return None

        
