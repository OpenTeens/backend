import requests


API_URI = "https://mail-admin.cxzlw.top"


def login():
    resp = requests.post(
        f"{API_URI}/api/login",
        {
            "username": "postmaster@openteens.org",
            "password": "5YoFj9lXknjXGGO3Vgpza7zY",
        },
    )

    cookie = resp.headers.get("Set-Cookie").split(";")[0].split("=")[1]

    return cookie


def user_create(username, passwd, quota):
    addr = username + "@openteens.org"
    resp = requests.post(
        f"{API_URI}/api/user/{addr}",
        {"name": username, "password": passwd, "quota": quota},
        cookies=LOGIN_COOKIE,
    )

    return resp.json()["_success"]


def user_delete(username):
    addr = username + "@openteens.org"
    resp = requests.delete(
        f"{API_URI}/api/user/{addr}",
        cookies=LOGIN_COOKIE,
    )

    return resp.json()["_success"]


def user_update(username, data):
    addr = username + "@openteens.org"
    resp = requests.put(
        f"{API_URI}/api/user/{addr}",
        data,
        cookies=LOGIN_COOKIE,
    )

    return resp.json()["_success"]


def user_get(username):
    addr = username + "@openteens.org"
    resp = requests.get(f"{API_URI}/api/user/{addr}", cookies=LOGIN_COOKIE)

    json = resp.json()

    if json["_success"]:
        return resp.json()["_data"]
    else:
        return None


if __name__ == "__main__":
    LOGIN_COOKIE = {"iRedAdmin-Pro-MYSQL": login()}
    user_create("test", "Test123!", 1024)
    # user_delete("test")
    user_update("test", {"quota": 2048})
