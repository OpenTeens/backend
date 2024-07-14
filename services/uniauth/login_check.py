from . import login_db
from . import token_db

def _uname_check(username: str):
    if len(username) < 6 or len(username) > 20:
        return False, "Username must be between 6 and 20 characters"
    
    if any(c not in "abcdefghijklmnopqrstuvwxyz0123456789_" for c in username):
        return False, "Username must only contain letters, numbers, and underscores"
    
    if not username[0].lower() in "abcdefghijklmnopqrstuvwxyz":
        return False, "Username must start with a letter"
    
    return True, ""
    

def register(username: str, password: str):
    check, msg = _uname_check(username)
    if check:
        check = login_db.register(username, password)

    if check:
        return {
            "code": 0,
            "token": token_db.create_token(username)    # there won't be 5 token when registering
        }
    else:
        return {
            "code": 1,
            "msg": msg or "Username already exists"
        }

def login(username: str, password: str):
    check, msg = _uname_check(username)
    if not check:
        return {
            "code": 1,
            "msg": msg
        }

    if not login_db.login(username, password):
        return {
            "code": 2,
            "msg": "Invalid username or password"
        }

    token = token_db.create_token(username)
    if token is None:
        return {
            "code": 3,
            "msg": "Too many tokens"
        }

    return {
        "code": 0,
        "token": token
    }

def tlogin(token: str):
    if not token_db.check_token(token):
        return {
            "code": 1,
            "msg": "Invalid token"
        }

    return {
        "code": 0,
        "username": token_db.get_username(token)
    }

def logout(token: str):
    if not token_db.check_token(token):
        return {
            "code": 1,
            "msg": "Invalid token"
        }

    if token_db.del_token(token):
        return {
            "code": 0
        }

    else:
        return {
            "code": 2,
            "msg": "Token not found"
        }
