import random
from hashlib import sha256


def genRandHash():
    return sha256(str(random.getrandbits(256)).encode()).hexdigest()
