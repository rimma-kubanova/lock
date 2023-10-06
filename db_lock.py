import sqlite3
from datetime import datetime, timedelta
from contextlib import contextmanager
        
class Lock:
    def __init__(self):
        self.create_table()
        
    @contextmanager        
    def connect(self):
        connection = sqlite3.connect("lock_servers_new.db")
        yield connection
        connection.close()
        

    def create_table(self):
        with self.connect() as connection:
            cursor=connection.cursor()
            cursor.execute(""" CREATE TABLE IF NOT EXISTS locks(
                id INTEGER PRIMARY KEY,
                lock_name TEXT,
                lock_owner TEXT,
                lock_time NUMERIC,
                expires_at NUMERIC
                )"""
            )
            
    def aquire(self, owner_name, lock_name, lock_duration=60):
        with self.connect() as connection:
            cursor = connection.cursor()
            
            
            expired_time = datetime.now() - timedelta(minutes=lock_duration)
            cursor.execute('DELETE FROM locks WHERE expires_at < ?', (expired_time,))
            # connection.commit()
            
            cursor.execute("SELECT * FROM locks WHERE lock_name = ?", (lock_name,))
            existing_lock = cursor.fetchone()
            
            if existing_lock:
                if existing_lock[2]==owner_name:
                    expires_at = datetime.now() + timedelta(minutes=lock_duration)
                    cursor.execute("UPDATE locks SET expires_at = ? WHERE id = ?", (expires_at, existing_lock[0]))
                    connection.commit()
                    print("existing lock/updating expired at")
                    return True
                else:
                    return False
            else:
                expires_at = datetime.now() + timedelta(minutes=lock_duration)
                cursor.execute('INSERT INTO locks (lock_name,lock_owner, lock_time,expires_at) VALUES (?,?,?,?)',
                            (lock_name, owner_name, datetime.now(), expires_at))
                print("new lock")
                connection.commit()
                return True
        
    # def release(connection):
    #     with connection:
    #         connection.execute("UPDATE tasks SET status=0 WHERE task_id =1")
        