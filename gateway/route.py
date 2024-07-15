import re
import urllib.parse


def urldecode(s):
    prev_s = ""

    while prev_s != s:
        prev_s = s
        s = urllib.parse.unquote(s)

    return s


class PathVar:
    def __init__(self, name, type):
        self.type = type or "string"
        self.name = name

    def match(self, s):
        if self.type == "string":
            return True

        elif self.type != "path":
            try:
                if self.type == "int":
                    int(s)
                elif self.type == "float":
                    float(s)
                return True
            except ValueError:
                return False

        else:
            raise NotImplementedError("Path type not implemented")


class RawRoute:
    def __init__(self, path):
        path = path.split("?")[0]  # remove query string
        path = path.lstrip("/")  # remove leading '/'
        path = path.split("/")  # split path into parts

        for i in range(len(path)):
            p = urldecode(path[i])
            m = re.match(
                r"^([a-zA-Z0-9\-_~.%]*)(<([a-zA-Z0-9\-_~.%]*:)?([a-zA-Z0-9\-_~.%]+)>)?([a-zA-Z0-9\-_~.%]*)$",
                p,
            )
            """
            match:
                - all chars are valid path chars (alpha, digit, '-', '_', '~', '.', '%')
                * [CAUTION]: special chars like '<', '>', ':' are also allowed (stricted by their position), to support route parameters
            """

            if not m:
                raise ValueError(f"Invalid path part: {p}")

            path[i] = {
                "prefix": m.group(1) or "",
                "param": m.group(2)
                and {
                    "type": m.group(3)[:-1] if m.group(3) else None,
                    "name": m.group(4),
                },
                "suffix": m.group(5) or "",
            }
            """
            path[i] = {
                "prefix": str,
                "param": None | {
                    "type": None | ["string" | "int" | "float" | "path"],
                    "name": str
                },
                "suffix": "" | str
            }
            """

        self.path = path

    def merge(self):
        """
        merge continuous 'const' path parts together
        """
        merged = []

        for p in self.path:
            if len(merged) != 0 and p["param"] is None and merged[-1]["param"] is None:
                merged[-1]["prefix"] += "/" + p["prefix"]
            elif p["param"] is not None and p["prefix"] != "":
                merged.append(
                    {
                        "prefix": merged[-1]["prefix"] + "/" + p["prefix"],
                        "param": None,
                        "suffix": "",
                    }
                )
                merged.append(
                    {"prefix": "", "param": p["param"], "suffix": p["suffix"]}
                )
            else:
                merged.append(p)

        m2 = []
        for p in merged:
            if p["param"] is None:  # const
                m2.append(p["prefix"])
            else:
                m2.append(PathVar(p["param"]["name"], p["param"]["type"]))

        return m2


class Route:
    def __init__(self, path: str, methods: list):
        self.path = RawRoute(path).merge()
        self.methods = methods


class RouteList:
    def __init__(self, routes: list):
        self.routes = []

        for i in range(len(routes)):
            r = routes[i]["path"]
            self.routes.append(Route(r, routes[i]["methods"]))

    def match(self, path: str, method: str):
        path = urldecode(path)
        path = path.split("?")[0]
        path = path.lstrip("/")
        path_backup = path

        matched = []

        for i in range(len(self.routes)):
            route = self.routes[i]
            rpath = route.path

            if method not in route.methods:
                continue

            path = path_backup
            params = {}

            for p in rpath:
                # 'const string' part: must be fully matched
                if type(p) is str:
                    if path.startswith("/"):
                        path = path[1:]
                    if path.startswith(p):
                        path = path[len(p):]
                # path variable part: match and extract
                elif type(p) is PathVar:
                    if p.type != "path":
                        path = path.lstrip("/")
                        part = path.split("/")[0]

                        if p.match(part):
                            params[p.name] = part  # extract
                            path = path[len(part) :]
                        else:
                            # not matched
                            break
                    else:
                        # TODO: doesn't support path type yet
                        pass
                # you should never reach here
                else:
                    raise ValueError("Invalid route part")
            else:
                if path.strip() == "":
                    matched.append([i, params])
                    return matched  # Due to the logic of flask routing (return the first matched route), we can simply return here.

        # return all matched routes
        return matched


if __name__ == "__main__":
    rl = RouteList(
        [
            {"path": "/", "methods": ["GET"], "handler": "index"},
            {"path": "/hello/<name>/<int:age>", "methods": ["GET"], "handler": "hello"},
        ]
    )

    m = rl.match("/hello/John/8", "GET")
    print(m)
