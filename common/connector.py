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

        uid = str(uid)
        random_string = Itaken.unique_string(10)

        from datetime import datetime
        add_time = datetime.now().isoformat(" ")

        access_token = Itaken.enmd5(uid + random_string + "AccessToken" + add_time)
        session_token = Itaken.enmd5(uid + random_string + "SessionToken" + add_time)

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
            # 处理 注册时间
            update_time = token_info["update_time"]
            token_info["update_time"] = update_time.isoformat(" ")

        return token_info
