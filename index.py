#!/usr/bin/python3
# -*- coding: utf-8 -*-
import web
from common.itaken import Itaken
from common.members import Member

urls = (
    '/login', 'login',
    '/', 'index'
)

render = web.template.render('templates/')
application = web.application(urls, globals())


class index:
    def GET(self):
        # uid = Member.register('admin', 'admin')

        uid = Member.login('admin', 'admin')
        # db = web.database(dbn="mysql", db="python-demo", user="root", pw="regel@123")
        # uid = Itaken.enpsw("admin")
        # uid = db.insert("members", name="regel", password=psw)
        # members = db.select("members")
        # str = ""
        # for mb in members:
        #     str += mb.id

        return uid, type(uid), "Hello world"
        # args = web.input()
        # return render.index(args.name)


class login:
    def GET(self):
        return render.login()

    def POST(self):
        args = web.input()
        if args.identity is None or args.identity == "":
            return Itaken.jsonreturn("", "账号不能为空")

        if args.password is None or args.password == "":
            return Itaken.jsonreturn("", "密码不能为空")

        return args.identity, args.password


if __name__ == "__main__":
    application.run()
