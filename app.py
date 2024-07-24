from gateway.apigateway import APIGateway

gateway = APIGateway(debug=True)
app = gateway.app

if __name__ == "__main__":
    gateway.run()
