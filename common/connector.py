#!/usr/bin/python3
# -*- coding: utf-8 -*-
import web
import config.db as dbconfig
from common.itaken import Itaken

# 连接数据库
db = web.database(dbn="mysql", db=dbconfig.MYSQL_DBNAME,
                  user=dbconfig.MYSQL_USERNAME, pw=dbconfig.MYSQL_PASSWORD)


# token类
# @author itaken<regelhh@gmail.com>
# @since 2017-07-28
class Connector:

    # 生成 token
    @classmethod
    def generate(cls, uid):
        uid = int(uid)
        if uid < 1:
            return None

        uid_str = str(uid)
        random_string = Itaken.unique_string(10)
        add_time = Itaken.nowtime()

        access_token = Itaken.enmd5(uid_str + random_string + "AccessToken" + add_time)
        session_token = Itaken.enmd5(uid_str + random_string + "SessionToken" + add_time)

        params = dict(uid=uid, access_token=access_token, session_token=session_token)
        sql = "REPLACE INTO ita_connector (uid,access_token,session_token,update_time)" \
              " VALUES ($uid,$access_token,$session_token,NOW())"
        res = db.query(sql, vars=params)
        if res:
            return {
                "code": 1,
                "uid": uid,
                "access_token": access_token,
                "session_token": session_token,
            }

        return {"code": 0, "message": "生成TOKEN失败"}

    # 获取用户TOKEN信息
    @classmethod
    def get_user_token_info(cls, uid):
        uid = int(uid)
        if uid < 1:
            return None

        result = db.select("ita_connector", where=dict(uid=uid))

        if not result:  # 结果不存在
            return None

        token_info = dict(result[0])

        if token_info.get("update_time"):
            # 处理 更新时间
            update_time = token_info["update_time"]
            token_info["update_time"] = update_time.isoformat(" ")

        return token_info

    # 更新 session_token
    @classmethod
    def update_session_token(cls, uid):
        uid = int(uid)
        if uid < 1:
            return None

        uid_str = str(uid)
        random_string = Itaken.unique_string(10)
        add_time = Itaken.nowtime()

        session_token = Itaken.enmd5(uid_str + random_string + "SessionToken" + add_time)

        result = db.update("ita_connector", where=dict(uid=uid), session_token=session_token)
        if result:
            return {"code": 1, "session_token": session_token}

        return {"code": 0}

    # 更新 access_token
    @classmethod
    def update_access_token(cls, uid):
        uid = int(uid)
        if uid < 1:
            return None

        uid_str = str(uid)
        random_string = Itaken.unique_string(10)
        add_time = Itaken.nowtime()

        access_token = Itaken.enmd5(uid_str + random_string + "AccessToken" + add_time)

        result = db.update("ita_connector", where=dict(uid=uid), access_token=access_token)
        if result:
            return {"code": 1, "access_token": access_token}

        return {"code": 0}

    # 加密 token
    @classmethod
    def encrypt_token(cls, uid, access_token, session_token):
        if access_token == "" or session_token == "":
            return {}

        uid = int(uid)
        if uid < 17:  # 防止出现 id 过小的情况
            uid = uid * 19

        if len(access_token) < 32:  # 防止出现长度不足的情况
            access_token = Itaken.enmd5(access_token)
        if len(session_token) < 32:
            session_token = Itaken.enmd5(session_token)

        session_token_list = list(session_token)  # token string转list
        str_key = access_token[8:20]  # 字符替换key

        pos = []
        mod_key = (11, 3, 7, 13, 5, 17)  # 求模key
        for index, i in enumerate(mod_key):
            chart = access_token[index: index + 1]  # 随机数
            point = (uid + int("0x" + chart, 16)) % i  # 获取的位置(16进制转10进制)

            pos = Itaken.spread_list(point, pos, 3, 1)  # 计算前半段
            pos = Itaken.spread_list(point + 16, pos, 3, 1)  # 计算后半段

        for index, i in enumerate(pos):
            session_token_list[i] = str_key[index]  # 密钥替换

        token = "".join(session_token_list)  # 加密后token

        return {
            "position": pos,
            "key": str_key,
            "token": token
        }

    # 验证 token
    @classmethod
    def verify_token(cls, uid, token):
        uid = int(uid)
        if uid < 1 or token == "" or token is None:
            return {"code": 0, "message": "验证内容不合法"}

        token_info = cls.get_user_token_info(uid=uid)
        if not token_info:
            return {"code": 0, "message": "没有该用户"}

        encrypt_info = cls.encrypt_token(uid=uid, access_token=token_info["access_token"], session_token=token_info["session_token"])
        if token == encrypt_info["token"]:
            return {"code": 1, "message": "验证成功", "uid": uid}

        token_list = list(token)  # token 转list
        token_key = ""
        for i in encrypt_info["position"]:
            token_key += token_list[i]  # 组装密钥

        if token_key == encrypt_info["key"]:
            return {"code": -1, "message": "session token失效"}

        return {"code": -2, "message": "access token失效"}
