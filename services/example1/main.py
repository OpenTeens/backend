def index(data):
    return 'Hello, world!'

def loginStatus(data):
    return str(data["prev_process"]["pipe_auth"]["authorized"])

def hello(data, name, age):
    if data["prev_process"]["pipe_auth"]["authorized"]:
        name = data["prev_process"]["pipe_auth"]["username"]
    return f'Hello, {name} ({age})'

if __name__ == '__main__':
    print(hello({}, "hg", 16))
