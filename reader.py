import evdev


class Reader:
    def __init__(self, path):
        self._dev = evdev.InputDevice(path)
        self._dev.grab()

    def read(self):
        keys = "X^1234567890XXXXqwertzuiopXX\nXasdfghjklXXXXXyxcvbnmXXXXXXXXXXXXXXXXXXXXXXX"
        code = ""
        for event in self._dev.read_loop():
            if event.type == 1 and event.value == 1:
                if event.code != 28:
                    code += keys[event.code]
                if event.code == 28:
                    try:
                        user_id = int(code)
                    except:
                        print "invalid code"
                    else:
                        yield user_id

                    code = ""