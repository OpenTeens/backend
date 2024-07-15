import importlib
import sys
import os
import json

from .route import RouteList

sys.path.append(f"{os.getcwd()}/services")


class Service:
    def __init__(self, meta: dict, apis: dict):
        self.meta = meta

        self.name = meta["name"]
        self.version = meta["version"]
        self.port = meta["port"]
        self.prefix = meta["prefix"]
        self.process = meta["process"]
        self.processType = meta["process"]["type"]
        self.disabled = meta.get("disabled", False)

        self.apis = apis
        self.routes = RouteList(apis["routes"])

        if self.disabled:
            return

        # forward request to a pymodule: import it
        if self.processType == "pymodule":
            self.module = self.import_pymodule()

    @classmethod
    def from_sname(cls, sname: str):
        meta = json.load(open(f"services/{sname}/meta.json"))
        apis = json.load(open(f"services/{sname}/apis.json"))

        return cls(meta, apis)

    def import_pymodule(self):
        module_name = self.name

        module = importlib.import_module(module_name)

        return module
