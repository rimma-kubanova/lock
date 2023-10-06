import db_lock
from time import sleep
from datetime import datetime
from croniter import croniter


next_time_to_execute = datetime.now()
cron_execute_every_hour = '* */1 * * *'


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
            with db_lock.context() as connection:
                if db_lock.aquire(connection):
                    run_task()
                    # db_lock.release(connection)
                else:
                    print("queue: task is already running")
            cron = croniter(cron_execute_every_hour, current_time)
            next_time_to_execute = cron.get_next(datetime)
        sleep(1)
        


if __name__ == "__main__":
    main_loop()
