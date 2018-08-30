class DummyLock:
    def __init__(self, lock_id):
        self.id = lock_id
        pass

    @staticmethod
    def open():
        print("open")
