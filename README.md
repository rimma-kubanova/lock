# Lock

This project implements lock mechanism using a database that ensures only one server performs task at a given time.

## Requirements/Versions
  Python 3.x
  SQLite3
  croniter 1.4.1
  psycopg2-binary 2.9.9
  python-dateutil 2.8.2
  six 1.16.0
  
## Installing

1. Clone the repository:
   ```bash
    git clone https://github.com/rimma-kubanova/lock.git
2. Navigate to the project directory
   ```bash
    cd lock
3. Install requirements
   ```bash
    pip3 install -r text_req.txt

## Running the code
  ```bash
  python3 test_task.py
  ```

## Database Structure

 - `lock_name`: The name of the lock for task (e.g, "backup")
  - `lock_owner`: The server running the task (e.g, "server-1")
  - `lock_time`: Timestamp showing when the lock was acquired
  - `expires_at`: Timestamp showing when the lock expires (usually `lock_time + 60` minutes)

## Case 1
<img width="1079" alt="Screenshot 2023-10-07 at 01 03 17" src="https://github.com/rimma-kubanova/lock/assets/115300909/5b529f5f-b095-40cd-a96c-bf8ffa5cd284">

When `server-1` runs the task, it follows the process below: 
-  The task is set to execute every minute (it is for testing purposes, in action, it would be 60 min) 
-  When initially executed, a new lock is created in the database
-  For the next executions, the existing lock is refreshed. Lock expiration date (`expires_at`) is updated
-  "new lock" indicates that a new lock is created (Step 2), and "existing lock/updating expired at" shows that the lock already exists and updated by its owner (Step 3)

## Case 2
<img width="1079" alt="Screenshot 2023-10-07 at 01 03 37" src="https://github.com/rimma-kubanova/lock/assets/115300909/a1aff183-22fc-4a9a-a3f0-1df826a5258d">

`server-2` attempts to run the same task.
- However, as the task was already executed by server-1 and the lock is not expired, server-2 will not execute the task
- "queue: the task is already running" indicates that the db_lock.aquire() function returned False

## Case 3
<img width="1079" alt="Screenshot 2023-10-07 at 01 05 45" src="https://github.com/rimma-kubanova/lock/assets/115300909/eb2fdd9c-9e09-42ea-887a-ae7b995d906c">

For testing purposes, I ran five programs using threading:
- Despite 5 servers running at the same time, one server executes the task
