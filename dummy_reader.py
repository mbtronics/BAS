from sys import stdin


class DummyReader:
    def __init__(self):
        pass

    @staticmethod
    def read():
        while True:
            yield stdin.read()