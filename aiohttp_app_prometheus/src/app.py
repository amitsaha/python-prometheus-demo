from aiohttp import web
import asyncio

async def test(request):
    return web.Response(text='test')

async def test1(request):
    1/0

@asyncio.coroutine
def error_middleware(app, handler):

    @asyncio.coroutine
    def middleware_handler(request):
        try:
            response = yield from handler(request)
            return response
        except web.HTTPException as ex:
            resp = web.Response(body=str(ex), status=ex.status)
            return resp
        except Exception as ex:
            resp = web.Response(body=str(ex), status=500)
            return resp



    return middleware_handler
if __name__ == '__main__':
    app = web.Application(middlewares=[error_middleware])
    app.router.add_get('/test', test)
    app.router.add_get('/test1', test1)
    web.run_app(app, port=8080)
