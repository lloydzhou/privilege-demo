import functools
import asyncio
import tornado

all_handlers = set()

def authenticated(method):
    fullname = '.'.join([method.__module__, method.__qualname__])
    all_handlers.add(fullname)
    print('authenticated', fullname, all_handlers)
    @functools.wraps(method)
    async def wrapper(self, *args, **kwargs):
        # 则先检查这个handler对应的method是否有配置权限
        # 如果配置了特殊的权限，则需要当前用户有权限才能访问。
        privilege = self.get_privilege(fullname)
        if len(privilege) and not len(privilege & self.session.get('privilege', [])):
            raise Exception('not allowed')
        return await method(self, *args, **kwargs)
    return wrapper


class MainHandler(tornado.web.RequestHandler):
    session = {
        'privilege': set([
            # 注释掉之后模拟没有权限的过程
            # 'show_main_page'
        ])
    }

    def get_privilege(self, fullname):
        # 这里返回name对应的权限名称
        # 通常一个权限名称，会对应一组handler（每一个handler实际就是一个fullname）
        return set([
            'show_main_page'
        ])

    @authenticated
    async def get(self):
        self.render('template/index.html')

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

async def main():
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())


