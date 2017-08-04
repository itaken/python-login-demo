#!/usr/bin/python3
# -*- coding: utf-8 -*-
import web
import config.db as dbconfig
from common.itaken import Itaken

# 连接数据库
db = web.database(dbn="mysql", db=dbconfig.MYSQL_DBNAME,
                  user=dbconfig.MYSQL_USERNAME, pw=dbconfig.MYSQL_PASSWORD)


# 用户类
# @author itaken<regelhh@gmail.com>
# @since 2017-07-24
class Member:

    # 用户注册
    @classmethod
    def register(cls, name="", psw=""):
        if name is None or name == "":
            return {"code": 0, "message": "用户名为空"}

        if psw is None or psw == "":
            return {"code": 0, "message": "密码为空"}

        # 判断用户是否存在
        is_exist = cls.is_user_exist(name=name)
        if is_exist < 1:
            return {"code": 0, "message": "该用户名已存在"}

        enname = Itaken.enmd5(name)  # 昵称hash
        psw = Itaken.enpsw(psw)  # 密码加密
        # 注册时间
        from datetime import datetime
        add_time = datetime.now().isoformat(" ")
        # add_time = SQLLiteral('NOW()')
        uid = db.insert("ita_members", name=name, enname=enname, password=psw, add_time=add_time)

        if uid:
            return {"code": 1, "message": "注册成功", "uid": uid}

        return {"code": 0, "message": "注册失败"}

    # 是否用户存在
    @classmethod
    def is_user_exist(cls, name):
        if name is None or name == "":
            return False

        enname = Itaken.enmd5(name)  # 昵称hash
        user = cls.__get_user_info(where=dict(enname=enname), field="uid")

        if user:
            uid = user.get("uid")
            return int(uid)

        return 0

# 用户登录
    @classmethod
    def login(cls, name, psw):
        if name is None or name == "":
            return {"code": 0, "message": "用户名为空"}

        if psw is None or psw == "":
            return {"code": 0, "message": "密码为空"}

        enname = Itaken.enmd5(name)  # 昵称hash
        psw = Itaken.enpsw(psw)  # 密码加密
        user = cls.__get_user_info(where=dict(enname=enname, password=psw))

        if user is None:
            return {"code": 0, "message": "账号或密码错误"}

        return {
            "code": 1,
            "uid": user.get("uid"),
            "name": user.get("name"),
        }

    # 获取用户信息
    @classmethod
    def __get_user_info(cls, where=None, field=None):
        if field is None or field == "":
            field = "*"

        if where is None or where == "":
            result = db.select("ita_members", what=field)
        else:
            result = db.select("ita_members", where=where, what=field)

        if not result:  # 结果不存在
            return None

        user = dict(result[0])

        if user.get("password"):
            user.pop("password")  # 删除密码项

        if user.get("add_time"):
            # 处理 注册时间
            add_time = user["add_time"]
            user["add_time"] = add_time.isoformat(" ")

        return user

    # 通过昵称获取用户信息
    @classmethod
    def get_user_info_by_name(cls, name, field=None):
        if name is None or name == "":
            return {"code": 0, "message": "用户名为空"}

        enname = Itaken.enmd5(name)  # 昵称hash
        user = cls.__get_user_info(where=dict(enname=enname), field=field)

        if user is None:
            return {"code": 0, "message": "没有该用户信息"}

        user["code"] = 1
        return user

    # 通过 uid 获取用户信息
    @classmethod
    def get_user_info_by_uid(cls, uid, field=None):
        if uid is None or uid == "":
            return {"code": 0, "message": "用户ID为空"}

        uid = int(uid)
        if uid < 1:  # 判断是否是int
            return {"code": 0, "message": "用户ID不合法"}

        user = cls.__get_user_info(where=dict(uid=uid), field=field)

        if user is None:
            return {"code": 0, "message": "没有该用户信息"}

        user["code"] = 1
        return user
