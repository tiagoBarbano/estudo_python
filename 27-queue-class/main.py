import time
from queue import Empty, Queue
from threading import Thread


def producer(queue):
    for i in range(1, 6):
        print(f'Inserting item {i} into the queue')
        time.sleep(1)
        queue.put(i)


def consumer(queue):
    while True:
        try:
            item = queue.get()
        except Empty:
            continue
        else:
            print(f'Processing item {item}')
            time.sleep(2)
            queue.task_done()


def main():
    queue = Queue()

    # create a producer thread and start it
    producer_thread = Thread(
        target=producer,
        args=(queue,)
    )
    producer_thread.start()

    # create a consumer thread and start it
    consumer_thread = Thread(
        target=consumer,
        args=(queue,),
        daemon=True
    )
    consumer_thread.start()

    # wait for all tasks to be added to the queue
    producer_thread.join()

    # wait for all tasks on the queue to be completed
    queue.join()


if __name__ == '__main__':
    main()