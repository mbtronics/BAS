import time


class DummyLock:
    def __init__(self, lock_id):
        self.id = lock_id
        pass

    @staticmethod
    def open(pulse_time_s=1):
        print("open")
        time.sleep(pulse_time_s)
        print("close")
