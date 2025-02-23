import threading
import queue
import random
import time
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


class MultithreadingSimulator:

    def __init__(self, maxsize: int = 10) -> None:
        """ Initializes the MultithreadingSimulator with a queue and a lock.

        Args:
            maxsize: Maximum size of the queue. Defaults to 10.
        """
        self.q = queue.Queue(maxsize=maxsize)
        self.lock = threading.Lock()
        self.stop_event = threading.Event()

    def producer(self) -> None:
        """ Produces random integers and places them in the queue every 0.1 seconds.
        """
        while not self.stop_event.is_set():
            num = random.randint(1, 100)
            with self.lock:
                if not self.q.full():
                    self.q.put(num)
                    logging.info(f'Produced: {num}')
            time.sleep(0.1)

    def consumer(self) -> None:
        """ Consumes integers from the queue and prints them every 0.15 seconds.
        """
        while not self.stop_event.is_set():
            with self.lock:
                if not self.q.empty():
                    num = self.q.get()
                    logging.info(f'Consumed: {num}')
            time.sleep(0.15)

    def run(self, duration: int = 10) -> None:
        """ Starts the producer and consumer threads and runs them for a specified duration.

        Args:
            duration: Duration in seconds to run the producer and consumer threads. Defaults to 10.
        """
        producer_thread = threading.Thread(target=self.producer, daemon=True)
        consumer_thread = threading.Thread(target=self.consumer, daemon=True)

        producer_thread.start()
        consumer_thread.start()

        time.sleep(duration)
        self.stop_event.set()

        producer_thread.join()
        consumer_thread.join()
        logging.info('Terminating program.')


def main() -> None:
    """ Main function to run the MultithreadingSimulator.
    """
    mts = MultithreadingSimulator()
    mts.run()


if __name__ == '__main__':
    main()
