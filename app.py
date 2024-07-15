import flask

from gateway.apigateway import APIGateway

def run(self):
    def make_gateway(s):
        def gateway(path):
            return self.process(s, path, flask.request)

        return gateway

    for _, s in self.services.items():
        self.app.route(
            f"/{s.prefix}/<path:path>",
            methods=["GET", "POST", "PUT", "DELETE"],
            endpoint=f"gw_{s.prefix}",
        )(make_gateway(s))


gateway = APIGateway()
run(gateway)
app = gateway.app
