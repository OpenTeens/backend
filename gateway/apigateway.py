import flask
import os
import json

from service import Service
from flask import Blueprint

class APIGateway:
    def __init__(self, host="0.0.0.0", port=5000):
        self.app = flask.Flask("API Gateway")
        self.services = self.get_all_services()
        self.host = host
        self.port = port

    def get_all_services(self) -> dict:
        """
        Find all services in the services directory and return their metadata.
        """
        slist = os.listdir("services")
        services = {}

        for s in slist:
            if os.path.isdir(f"services/{s}"):
                if os.path.exists(f"services/{s}/meta.json"):
                    with open(f"services/{s}/meta.json", "r") as f:
                        meta = json.load(f)
                    with open(f"services/{s}/apis.json", "r") as f:
                        apis = json.load(f)

                    sname = meta["name"]
                    services[sname] = Service(meta, apis)

        return services
    
    def run(self):
        # Register the API blueprints
        for _, s in self.services.items():
            if not s.disabled:
                for s in self.services.items():
                    if not s.disabled:
                        blueprint = s.create_blueprint(self.gen_gateway)
                        self.app.register_blueprint(blueprint)

        self.app.run(self.host, self.port)

    def gen_gateway(self, service: Service):
        def gateway(path, request):
            return f"Hello from {service.name} at {path}, {request.method}!"
        
        return gateway

if __name__ == "__main__":
    apigate = APIGateway("0.0.0.0", 5000)
    apigate.run()