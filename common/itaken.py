#!/usr/bin/python3
# -*- coding: utf-8 -*-
import web


# 公共方法
# @author itaken<regelhh@gmail.com>
# @since 2017-07-21
class Itaken:

    # JSON 数据返回
    @classmethod
    def jsonreturn(cls, data, message="SUCCESS", code=1):
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
    def enmd5(cls, data):
        data = str(data) + "4ITAKEN:)"
        import hashlib
        data = hashlib.md5(data.encode("UTF-8")).hexdigest()  # 昵称hash
        return data

    # 生产密码hash
    @classmethod
    def enpsw(cls, raw_psw):
        import hashlib
        raw_psw = str(raw_psw)
        sha256 = hashlib.sha256(raw_psw.encode("UTF-8")).hexdigest()
        raw_psw = (raw_psw + "ITAKEN@GIT;)" + sha256).encode("UTF-8")
        hsh = hashlib.md5(raw_psw).hexdigest()
        return hsh

    # 生产唯一字符串
    @classmethod
    def unique_string(cls, strlen=6):
        strlen = int(strlen)
        if strlen < 1:
            return None
        import uuid
        return uuid.uuid4().hex[:strlen].upper()
