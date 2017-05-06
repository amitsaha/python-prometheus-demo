import prometheus_client

from aiohttp import web
from helpers.middleware import error_middleware, setup_metrics


async def test(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

async def test1(request):
    1/0

async def metrics(request):
    resp = web.Response(body=prometheus_client.generate_latest())
    resp.content_type = prometheus_client.CONTENT_TYPE_LATEST
    return resp

if __name__ == '__main__':
    app = web.Application(middlewares=[error_middleware])
    setup_metrics(app, "webapp_1")
    app.router.add_get("/metrics", metrics)
    app.router.add_get('/test', test)
    app.router.add_get('/test1', test1)

    web.run_app(app, port=8080)
