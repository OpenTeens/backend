import flask
import os
import json
import yaml

from .service import Service
from .pipe import Pipe
from flask_cors import CORS


class APIGateway:
    def __init__(self, host="0.0.0.0", port=5000, **kwargs):
        self._get_all_services()
        self.pipe = Pipe(yaml.load(open("gateway/pipe.yaml"), yaml.SafeLoader))

        self.app = flask.Flask("API Gateway")

        CORS(self.app, origins=["https://openteens.org", "https://todo.openteens.org"])

        self.host = host
        self.port = port
        self.kwargs = kwargs

        self.create_gateway_routes()

    def _get_all_services(self):
        """
        Find all services in the services directory and return their metadata.
        """
        slist = os.listdir("services")
        services = {}

        for s in slist:
            meta = json.load(open(f"services/{s}/meta.json"))
            apis = json.load(open(f"services/{s}/apis.json"))

            sname = meta["name"]
            services[sname] = Service(meta, apis)

        self.services = services

    def create_gateway_routes(self):
        """
        Creates the gateway routes for all registered services.

        This method iterates over all registered services and creates the gateway routes
        for each service. The gateway routes are created using the Flask `route` decorator
        and the `make_gateway` function.

        The `make_gateway` function is a closure that takes a service `s` as input and returns
        a gateway function. The gateway function takes a `path` parameter and calls the `process`
        method of the `self` object with the service `s`, the `path`, and the Flask `request` object.

        The gateway routes are created for the HTTP methods GET, POST, PUT, and DELETE, and the
        endpoint name is set to `gw_<service_prefix>`.

        Example usage:
        ```
        gateway = ApiGateway()
        gateway.create_gateway_routes()
        ```
        """

        def make_gateway(s):
            def gateway(path):
                return self.process(s, path)

            return gateway

        for _, s in self.services.items():
            self.app.route(
                f"/{s.prefix}/<path:path>",
                methods=["GET", "POST", "PUT", "DELETE"],
                endpoint=f"gw_{s.prefix}",
            )(make_gateway(s))

    def run(self):
        self.app.run(self.host, self.port, **self.kwargs)

    def process(self, service: Service, path):
        """
        Process a incoming request, and return the response
        """
        # route
        m = service.routes.match(path, flask.request.method)
        if not m:
            print("Not matched:", path)
            flask.abort(404)
        api_id, params = m[0]  # the first matched
        api = service.apis["routes"][api_id]

        # pipe
        res = self.pipe.process(f"/{service.prefix}/{path}", flask.request.method, api)
        if res is False:
            flask.abort(403)
        prev_process = res

        # process
        if service.processType == "pymodule":
            return self.process_pymodule(service.module, api, params, prev_process)

    def process_pymodule(self, module, api, params: dict, prev_process: dict):
        """
        Process a incoming request using specified module, which containes the handler.
        """
        handler_name = api["handler"]
        handler_func = getattr(module, handler_name)

        response = handler_func(prev_process, **params)
        return response


if __name__ == "__main__":
    apigate = APIGateway("0.0.0.0", 5000, debug=True)
    apigate.run()
