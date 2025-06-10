import hashlib
import sqlite3

USER_TABLE = 'users'
REGISTRATION_TABLE = 'registrations'
SUBJECT_TABLE = 'subjects'


class Database:
    def __init__(self, db_name='database.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self) -> None:
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ? (
                user_id INTEGER PRIMARY KEY,
                password_hash TEXT NOT NULL,
            )
        ''', (USER_TABLE,))
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ? (
                user_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                evaluation TEXT NOT NULL,
                passed BOOLEAN NOT NULL
            )
        ''', (REGISTRATION_TABLE,))
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ? (
                subject_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        ''', (SUBJECT_TABLE,))
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()

    def add_user(self, user_id, password) -> None:
        password_hash = hash_password(password)
        self.cursor.execute('''
            INSERT INTO ? (user_id, password_hash)
            VALUES (?, ?)
        ''', (USER_TABLE, user_id, password_hash))
        self.connection.commit()

    def delete_user(self, user_id) -> None:
        self.cursor.execute('''
            DELETE FROM ? WHERE user_id = ?
        ''', (USER_TABLE, user_id))
        self.connection.commit()

    def check_user(self, user_id, password) -> bool:
        password_hash = hash_password(password)
        self.cursor.execute('''
            SELECT * FROM ? WHERE user_id = ? AND password_hash = ?
        ''', (USER_TABLE, user_id, password_hash))
        return self.cursor.fetchone() is not None

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()
