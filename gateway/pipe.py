import re

from .service import Service

class PipeItem:
    def __init__(self, config: dict):
        self.config = config

        self.name = config["name"]
        self.rules = config["rules"]

        # processor
        processor = config["processor"]
        self.processor = Service.from_sname(processor["service"])
        self.handler = getattr(self.processor.module, processor["handler"])

    def match(self, path: str, method: str):
        """
        Match a path and a method to a pipe item
        """
        for r in self.rules:
            if r["methods"] == "*" or method in r["methods"]:
                print(r["path"], path)
                if re.match(r["path"], path):
                    return True

        return False
    
    def process(self, prev_data: dict):
        """
        Process a incoming request, and return the response
        """
        result = self.handler(prev_data)

        if result["reject"]:
            return False
        else:
            data = result["result"]
            return data


class Pipe:
    def __init__(self, config: dict):
        self.config = config

        self.items = []
        for i in config["pipes"]:
            self.items.append(PipeItem(i))

    def process(self, fullPath: str, method: str):
        """
        Process a incoming request, and return the response
        """
        prev_process = {}

        for item in self.items:
            if item.match(fullPath, method):
                result = item.process(prev_process)
                if result is False:
                    return False
                
                for k, v in result.items():
                    prev_process[k] = v

        return prev_process

