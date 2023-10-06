import sqlite3
from contextlib import contextmanager
        
def can_aquire(connection):
    # check if the task is already acquired
    with connection:
        connection.execute('SELECT status FROM tasks WHERE task_id = 1')
        return not connection.cursor().fetchone()
        
def aquire(connection):
    if can_aquire(connection):
        with connection:
            # change status to acquired, if no change, 
            # then it is already running - return false
            connection.execute("UPDATE tasks SET status = 1 WHERE task_id = 1 AND status = 0")
            if connection.total_changes == 1:
                return True
            else:
                return False
        
    
def release(connection):
    with connection:
        connection.execute("UPDATE tasks SET status=0 WHERE task_id =1")

@contextmanager        
def context():
    # table to store the status of a task, status is either 0 or 1. 
    # 0 - can run, 1 - already running, hands off ! 
    connection = sqlite3.connect("lock_servers.db")
    with connection:
        table = """ CREATE TABLE IF NOT EXISTS tasks(
        task_id INTEGER PRIMARY KEY, 
        status INTEGER
        )"""
        connection.execute(table)
        lock = "INSERT OR IGNORE INTO tasks (task_id, status) VALUES(1, 0)"
        connection.execute(lock)
    try:
        yield connection
    finally:
        connection.close()