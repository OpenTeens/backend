import importlib.util

from route import RouteList


class Service:
    def __init__(self, meta: dict, apis: dict):
        self.meta = meta

        self.name = meta["name"]
        self.version = meta["version"]
        self.port = meta["port"]
        self.prefix = meta["prefix"]
        self.forward = meta["forward"]
        self.forwardType = meta["forward"]["type"]
        self.disabled = meta.get("disabled", False)

        self.apis = apis
        self.routes = RouteList(apis["routes"])

        if self.disabled:
            return
        
        # forward request to a pymodule: import it
        if self.forwardType == "pymodule":
            self.module = self.import_pymodule()

    def import_pymodule(self):
        module_name = f"service_{self.name}"
        module_path = self.forward["entry"]

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module
