def index(prev_process):
    return 'Hello, world!'

def loginStatus(prev_process):
    return str(prev_process["authorized"])

def hello(prev_process, name, age):
    if prev_process["authorized"]:
        name = prev_process["username"]
    return f'Hello, {name} ({age})'

if __name__ == '__main__':
    print(hello({}, "hg", 16))
