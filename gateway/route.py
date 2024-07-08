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


class Route:
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


class RouteList:
    def __init__(self, routes: list):
        self.routes = routes

        for i in range(len(routes)):
            r = routes[i]
            self.routes[i] = Route(r).merge()

    def match(self, path: str):
        path = urldecode(path)
        path = path.split("?")[0]
        path = path.lstrip("/")
        path_backup = path

        matched = []

        for i in range(len(self.routes)):
            route = self.routes[i]
            path = path_backup
            params = {}

            for p in route:
                # 'const string' part: must be fully matched
                if type(p) is str:
                    if path.startswith(route[0]):
                        path = path[len(route[0]) :]
                # path variable part: match and extract
                elif type(p) is PathVar:
                    # TODO: doesn't support path type yet
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
        ["/", "/hello", "/hello/world/<name>", "/hello/<to>/<name>", "bye/<name>"]
    )

    m = rl.match("/hello/world/John")
    print(m)
