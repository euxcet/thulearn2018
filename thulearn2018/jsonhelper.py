import json
import platform

class JsonHelper():
    def __init__(self):
        pass

    def loads(self, content):
        def is_windows():
            return platform.system() == 'Windows'
            
        result = {}
        try:
            if(is_windows()):
                result = json.loads(bytes.decode(content))
            else:
                result = json.loads(content)
        except Exception:
            print("密码错误")
            exit(1)
        return result
