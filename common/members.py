#!/usr/bin/python3
# -*- coding: utf-8 -*-
import web
import config.db as dbconfig
from common.itaken import Itaken
from common.connector import Connector

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
        add_time = Itaken.nowtime()  # 注册时间

        uid = db.insert("ita_members", name=name, enname=enname, password=psw, add_time=add_time)

        if uid:
            Connector.generate(uid=uid)  # 生成授权token
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

        uid = user.get("uid")
        token_info = Connector.get_user_token_info(uid=uid)
        if not token_info:  # 防止因为没有生成token导致的错误
            token_info = Connector.generate(uid=uid)
            session_token = token_info.get("session_token")
        else:
            update_res = Connector.update_session_token(uid=uid)  # 更新 登录token
            session_token = update_res.get("session_token")

        access_token = token_info.get("access_token")
        token_encrypt = Connector.encrypt_token(uid=uid, access_token=access_token, session_token=session_token)

        return {
            "code": 1,
            "uid": uid,
            "name": user.get("name"),
            "token": token_encrypt.get("token"),
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

    # 修改用户密码
    @classmethod
    def reset_psw(cls, uid, new_psw):
        # TODO::...
        Connector.update_access_token(uid=uid)  # 更新授权信息
