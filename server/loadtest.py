import urllib2 as u2
import random

from Queue import Queue
from threading import Thread

BASE_URL = "localhost:8080"
#BASE_URL = "tin-bronze2.appspot.com"

class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try: func(*args, **kargs)
            except Exception, e: print e
            self.tasks.task_done()

class ThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()


def main():
  pool = ThreadPool(10)
  def task():
    url = "http://" + BASE_URL + "/submit?temp=" + str(random.random() * 3 + 16)
    print url
    u2.urlopen(url)

  for i in range(0, 100):
    pool.add_task(task)

  pool.wait_completion()

if __name__ == '__main__':
  main()