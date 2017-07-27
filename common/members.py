#!/usr/bin/python3
# -*- coding: utf-8 -*-
import web
import config.db as dbconfig
from common.itaken import Itaken

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
        if cls.is_user_exist(name=name) != False:
            return {"code": 0, "message": "该用户名已存在"}

        enname = Itaken.hash(name)  # 昵称hash
        psw = Itaken.enpsw(psw)  # 密码加密
        uid = db.insert("members", name=name, enname=enname, password=psw)
        if uid:
            return {"code": 1, "message": "注册成功", "uid": uid}

        return {"code": 0, "message": "注册失败"}

    # 是否用户存在
    @classmethod
    def is_user_exist(cls, name=""):
        if name is None or name == "":
            return False

        user = cls.get_user_info_by_name(name=name, field="uid")

        if user.get("code") != 1:
            return False

        uid = user.get("uid")
        return int(uid)

    # 用户登录
    @classmethod
    def login(cls, name="", psw=""):
        if name is None or name == "":
            return {"code": 0, "message": "用户名为空"}

        if psw is None or psw == "":
            return {"code": 0, "message": "密码为空"}

        user = cls.get_user_info_by_name(name=name)
        if user.get("code") != 1:
            return user

        psw = Itaken.enpsw(psw)  # 密码加密
        if user.get("password") != psw:
            return {"code": 0, "message": "账号或密码错误"}

        return {
            "code": 1,
            "uid": user.get("uid"),
            "name": user.get("name"),
        }

    # 通过昵称获取用户信息
    @classmethod
    def get_user_info_by_name(cls, name, field=None):
        if name is None or name == "":
            return {"code": 0, "message": "用户名为空"}

        enname = Itaken.hash(name)  # 昵称hash
        sql_data = dict(enname=enname)
        if field is None or field == "" or field == "*":
            result = db.select("members", where=sql_data)
        else:
            result = db.select("members", where=sql_data, what=field)

        if result:
            user = dict(result[0])
            user["code"] = 1
            return user
        
        return {"code": 0, "message": "没有该用户信息"}
