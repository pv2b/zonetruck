from Queue import PriorityQueue
from threading import Thread

class WorkManager:
    def _worker():
        while True:
            item = q.get()
            if item is None:
                break
            priority, task, subsequentTasks = item
            taskResult = task()
            for subsequentTask in subsequentTasks[0]:
                # Prioritize getting the subtasks done higher than the task
                # itself. This ensures that we prioritize completing existing
                # tasks rather than growing our queue.
                self.submitWork(priority - 1, subsequentTask, subsequentTasks[1:])
            q.task_done()
            
    def __init__(self, num_workers):
        self.queue = self.PriorityQueue()
        self.threads = []
        self.num_workers = num_workers
    def submitWork(priority, task, subsequentTasks)
        while len(threads) < num_workers:
            t = Thread(target=self._worker)
            t.start()
            threads.append(t)
        self.queue.put((priority, task, subsequentTasks))
    def join():
        self.queue.join()
        # Put one sentinel on the queue for each thread, instructing all threads
        # to exit
        for t in threads:
            self.queue.put(None)
        for t in threads:
            t.join()
        self.queue = None
        self.threads = []
