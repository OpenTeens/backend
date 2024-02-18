"""
这里是功能文件, 也就是该service内部的业务逻辑, 不管你怎么写, 分成不同的文件也可以。
"""

def plus(a, b):
    """
    [tools] plus a and b
    """
    return a + b


def add(a, b):
    """
    add a and b

    :param a: int
    :param b: int

    :return: int
    """
    return plus(a, b)

def hlwd():
    """
    say hello world

    :return: str
    """
    return "Hello World!"
