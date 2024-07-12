import flask
import os
import json

from service import Service

class APIGateway:
    def __init__(self, host="0.0.0.0", port=5000, **kwargs):
        self._get_all_services()

        self.app = flask.Flask("API Gateway")
        self.host = host
        self.port = port
        self.kwargs = kwargs

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
    
    def run(self):
        """
        Create specified router from services' prefixes. And run the flask app
        """
        def make_gateway(s):
            def gateway(path):
                print(self.app.url_map)
                return self.process(s, path, flask.request)
            return gateway

        for _, s in self.services.items():
            self.app.route(f"/{s.prefix}/<path:path>", methods=["GET", "POST", "PUT", "DELETE"], endpoint=f"gw_{s.prefix}")(make_gateway(s))

        self.app.run(self.host, self.port, **self.kwargs)

    def process(self, service: Service, path, request: flask.Request):
        """
        Process a incoming request, and return the response
        """
        m = service.routes.match(path, request.method)
        if not m:
            print("Not matched:", path)
            flask.abort(404)
        
        api_id, params = m[0]   # the first matched
        api = service.apis["routes"][api_id]

        if service.processType == "pymodule":
            return self.process_pymodule(service.module, api, params)

    def process_pymodule(self, module, api, params: dict):
        """
        Process a incoming request using specified module, which containes the handler.
        """
        handler_name = api["handler"]
        handler_func = getattr(module, handler_name)

        response = handler_func(**params)
        return response

if __name__ == "__main__":
    apigate = APIGateway("0.0.0.0", 5000, debug=True)
    apigate.run()

