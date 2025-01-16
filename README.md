# 权限控制逻辑
1. 使用rbac那一套通过user拿到privilege：user -> role -> privilege
2. privilege代表一个权限
3. 一个privilege会对应一组handlers(actions)
4. 前后端两个装饰器，都是使用allow_handlers判断当前的handler在不在里面

