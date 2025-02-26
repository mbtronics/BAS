import evdev

class Reader:
    def __init__(self, path):
        self._dev = evdev.InputDevice(path)
        self._dev.grab()

    async def read(self):
        keys = "X^1234567890XXXXqwertzuiopXX\nXasdfghjklXXXXXyxcvbnmXXXXXXXXXXXXXXXXXXXXXXX"
        code = ""
        async for event in self._dev.async_read_loop():
            if event.type == 1 and event.value == 1:
                if event.code != 28:
                    code += keys[event.code]
                if event.code == 28:
                    try:
                        user_id = int(code)
                    except ValueError:
                        print("invalid code")
                    else:
                        yield user_id
                    code = ""
