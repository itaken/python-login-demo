#!/usr/bin/python3
# -*- coding: utf-8 -*-
import web


# 公共方法
# @author itaken<regelhh@gmail.com>
# @since 2017-07-21
class Itaken:

    # JSON 数据返回
    @classmethod
    def jsonreturn(cls, data, message="SUCCESS", code=200):
        import json
        ret = {
            "data": data,
            "message": message,
            "code": code
        }
        web.header("Content-Type", "application/json")
        return json.dumps(ret)

    # 获取Hash数据
    @classmethod
    def hash(cls, data):
        data = str(data)
        import hashlib
        data = hashlib.sha1(data.encode("UTF-8")).hexdigest()  # 昵称hash
        return data

    # 生产密码hash
    @classmethod
    def enpsw(cls, raw_psw):
        import hashlib
        raw_psw = str(raw_psw)
        sha256 = hashlib.sha256(raw_psw.encode("UTF-8")).hexdigest()
        raw_psw = (raw_psw + "ITAKEN@GIT;)" + sha256).encode("UTF-8")
        hsh = hashlib.sha1(raw_psw).hexdigest()
        return hsh
