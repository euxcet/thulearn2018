import json
from re import findall


class JsonHelper():
    def __init__(self):
        pass

    def loads(self, content):
        result = {}
        try:
            if isinstance(content, bytes):
                content = bytes.decode(content)
            result = json.loads(findall(r'({.*})', content)[0])
        except Exception:
            print("密码错误")
            exit(1)
        return result
