def index():
    return {"success": True, "msg": "hello, world!"}


def init(inter_router, exp_router):

    inter_router.add_api_route("/", index, methods=["GET"])

    exp_router.add_api_route("/example-service1/helloworld", index, methods=["GET"])
