from gateway.apigateway import APIGateway

gateway = APIGateway("0.0.0.0", 5009, debug=True)
app = gateway.app

if __name__ == "__main__":
    gateway.run()
