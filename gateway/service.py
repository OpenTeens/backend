from flask import Blueprint, request

import os

from route import RouteList


class Service:
    def __init__(self, meta: dict, apis: dict):
        self.meta = meta

        self.name = meta["name"]
        self.version = meta["version"]
        self.port = meta["port"]
        self.prefix = meta["prefix"]
        self.run = meta["run"]
        self.disabled = meta.get("disabled", False)

        self.routes = RouteList(apis["routes"])

        if not self.disabled:
            self.activate()

    def activate(self):
        match self.run["use"]:
            case "shell":
                os.system(f"{self.run['command']} &")

    def create_bp_normal(self, gateway: callable):
        """
        Create a Flask blueprint for API routes with the given prefix.
        """
        prefix = self.prefix
        blueprint = Blueprint(prefix, __name__, url_prefix=f"/{prefix}")

        # decorate the handler
        @blueprint.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
        def route_handler(path):
            return gateway(path, request)
        
        return blueprint
    
    def create_blueprint(self, gen_gateway: callable):
        creator = {
            "shell": self.create_bp_normal,
        }.get(self.run["use"], self.create_bp_normal)

        gateway = gen_gateway(self)

        return creator(gateway)
