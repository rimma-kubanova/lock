import db_lock
from time import sleep
from datetime import datetime
from croniter import croniter
import threading
import time

next_time_to_execute = datetime.now()
cron_execute_every_hour = '* */1 * * *'
owner_name = 'server 7'
def run_task():
    # Код который должен быть выполнен только 1 раз за час
    # только на 1 машине
    print("EXECUTED AT: ", datetime.now())


def main_loop():
    global next_time_to_execute
    while True:
        current_time = datetime.now()
        if current_time > next_time_to_execute:
            # Если db_lock.aquire() возвращает True
            # Значит выполнять код можно и никто кроме этой машины
            # его в данный момент не выполнит.
            # Здесь нет except значит рейзить ошибки нельзя
            if db_lock.aquire(owner_name,'backup_lock_5'):
                run_task()
            else:
                print("queue: task is already running")
            cron = croniter(cron_execute_every_hour, current_time)
            next_time_to_execute = cron.get_next(datetime)
        sleep(1)


# TESTING: runnning 5 tasks at the same time. Expecting 1 task to perform backup, others just skipping it.
def simulate(process_id):
    owner_name = f"server_{process_id}"
    
    if db_lock.aquire(owner_name,"new_lock"):
        print(f"{owner_name} acquired the lock & performing backup...")
        time.sleep(5)
        print(f"{owner_name} backup completed!")
    else:
        print(f"{owner_name} couldn't acquire the lock. Another process is already performing it")


if __name__ == "__main__":
    db_lock = db_lock.Lock()
    main_loop()
    
    
    # testing, simulating 5 tasks running at the same time using threading
    # processes = []
    # for i in range(1, 6):
    #     process = threading.Thread(target=simulate, args=(i,))
    #     processes.append(process)
    #     process.start()

    # for process in processes:
    #     process.join()