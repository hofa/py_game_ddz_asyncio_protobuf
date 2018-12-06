from aiohttp import web, ClientSession
import aioredis
import asyncio
connection = {}
async def redis_connect(loop):
    pool = await aioredis.create_pool(address=(str("192.168.10.57"), int(6379)),
                                                                    password="123456", 
                                                                    db=1, 
                                                                    encoding='utf-8',
                                                                    minsize=1, maxsize=10, loop=loop)
    connection["redis"] = pool

async def post(request):
    data = await request.post()
    print(data.get("b", "2222"))
    return web.Response(text='Hello World!2')

async def index(request):
    with await connection["redis"] as conn:
        await conn.execute('SET', "qq", "abcd")
    return web.Response(text='Hello World!2')

port = 10087
loop = asyncio.get_event_loop()
loop.run_until_complete(redis_connect(loop))
app = web.Application()
app.router.add_post('/', post)
app.router.add_get('/', index)
web.run_app(app, host='0.0.0.0', port=port)