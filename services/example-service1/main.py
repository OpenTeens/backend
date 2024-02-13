import flask

app = flask.Flask("example-service1")

@app.route('/')
def index():
    return 'Hello, world!'

if __name__ == '__main__':
    app.run("localhost", 5001)
