import threading

import random
import sys


class Worker(threading.Thread):
    """
    This class represents a basic worker to process tasks.
    Each worker should have a queue tu pull messages from.
    Each worker should have a writer to write tasks results.
    Each worker should have a db to persist tasks states.
    """
    def __init__(self, queue, writer, db, *args, **kwargs):
        super(Worker, self).__init__(*args, **kwargs)
        self.worker_id = random.randint(0, sys.maxsize)
        self.queue = queue
        self.writer = writer
        self.db = db


def run():
    """
    This method is responsible for pulling messages, processing it and persist the state of a task.
    :return:
    """
    raise NotImplementedError("A worker must implement a run method")
