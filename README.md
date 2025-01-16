# 权限控制逻辑
1. 使用rbac那一套通过user拿到privilege：user -> role -> privilege
2. privilege代表一个权限
3. 一个privilege会对应一组handlers(actions)
4. 前后端两个装饰器，都是使用allow_handlers判断当前的handler在不在里面

![image](https://github.com/user-attachments/assets/3314e34a-3100-49da-bd17-80c0b7500ab3)

