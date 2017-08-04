#!/usr/bin/python3
# -*- coding: utf-8 -*-
import web
from common.itaken import Itaken
from common.members import Member

from common.connector import Connector

urls = (
    '/login', 'login',
    '/', 'index'
)

render = web.template.render('templates/')
app = web.application(urls, globals())


# 主页
class index:
    def GET(self):
        uid = web.cookies().get("__uid")
        user = Member.get_user_info_by_uid(uid, "name")

        if user.get("code") == 0:
            raise web.seeother("/login")

        name = user.get("name")
        return render.index(name)


# 用户登录
class login:
    # 登录主页
    def GET(self):
        return render.login()

    # 登录POST
    def POST(self):
        args = web.input()
        identity = args.identity
        if identity is None or identity == "":
            return Itaken.jsonreturn("", "账号不能为空", 0)

        password = args.password
        if password is None or password == "":
            return Itaken.jsonreturn("", "密码不能为空", 0)

        result = Member.login(identity, password)
        if result.get("code") != 1:
            return Itaken.jsonreturn("", result.get("message"), 0)

        uid = result.get("uid")  # 用户ID
        # 成功, 设置cookie
        web.setcookie("__uid", uid, 7*86400)
        return Itaken.jsonreturn({"uid": uid}, "登录成功", 1)


if __name__ == "__main__":
    app.run()
