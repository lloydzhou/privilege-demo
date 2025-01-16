import functools
import asyncio
import tornado

all_handlers = set()

# 这里的映射关系可以放数据库
privileges = {
    'show_main_page': set([
        '__main__.MainHandler.get',
        # 后端可以把前端对应的也一起定义了
        'antd.Object.canClickLickButton',
        'antd.Object.canClickUnLickButton'
    ])
}


def authenticated(method):
    fullname = '.'.join([method.__module__, method.__qualname__])
    all_handlers.add(fullname)
    @functools.wraps(method)
    async def wrapper(self, *args, **kwargs):
        # 则先检查这个handler对应的method是否有配置权限
        # 如果配置了特殊的权限，则需要当前用户有权限才能访问。
        # 这里可以使用privilege判断，其实也可以直接使用handlers判断
        allow_handlers = self.get_allow_handlers()
        print()
        if isinstance(allow_handlers, set) and not fullname in allow_handlers:
            raise Exception('not allowed')
        return await method(self, *args, **kwargs)
    return wrapper


class MainHandler(tornado.web.RequestHandler):

    def get_allow_handlers(self):
        # 这里是需要按用户自己的角色对应的权限，再取交集
        # 注释之后模拟没有权限
        return privileges.get('show_main_page')
        return set()

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


