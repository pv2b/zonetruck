from queue import PriorityQueue
from threading import Thread
from math import inf
from traceback import print_exc

class WorkManager:
    _WORKER_EXIT_SENTINEL = (inf, None)
    def _worker(self):
        while True:
            item = self.queue.get()
            if item is WorkManager._WORKER_EXIT_SENTINEL:
                break
            priority, task, task_args, subsequent_tasks = item
            try:
                subsequent_task_args = task(*task_args)
                if subsequent_tasks:
                    for subsequent_task in subsequent_tasks[0]:
                        # Prioritize getting the subtasks done higher than the task
                        # itself. This ensures that we prioritize completing existing
                        # tasks rather than growing our queue.
                        self.submit_work(priority - 1,
                                        subsequent_task,
                                        subsequent_task_args,
                                        subsequent_tasks[1:])
            except:
                # TODO improve error handling
                print("Error handling task %r %r" % (task, task_args))
                print_exc()
            finally:
                self.queue.task_done()

    def __init__(self):
        self.queue = PriorityQueue()
        self.threads = []
    def submit_work(self, priority, task, task_args, subsequent_tasks):
        self.queue.put((priority, task, task_args, subsequent_tasks))
    def start(self, num_workers=4):
        while len(self.threads) < num_workers:
            thread = Thread(target=self._worker)
            thread.start()
            self.threads.append(thread)

    def join(self):
        self.queue.join()
        for thread in self.threads:
            self.queue.put(WorkManager._WORKER_EXIT_SENTINEL)
        for thread in self.threads:
            thread.join()
        self.queue = None
        self.threads = []
