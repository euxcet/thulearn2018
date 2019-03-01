import json

class JsonHelper():
    def __init__(self):
        pass

    def loads(self, content):
        result = {}
        try:
            result = json.loads(content)
        except TypeError:
            result = json.loads(bytes.decode(content))
        except Exception:
            print("密码错误")
            exit(1)
        return result
