#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests
import unittest
from util.request_util import RequestUtil
'''
@Project ：test 
@File    ：UserTsetCase.py
@Author  ：jijianfeng
@Date    ：2021/6/30 下午3:08 
'''
host = "https://api.xdclass.net"
class UserTestCase(unittest.TestCase):
    def testLogin(self):
        url = host + "/pub/api/v1/web/web_login"
        data = {"phone": "15737314581", "pwd": "13519553700jjf"}
        headers ={"Content-Type":"application/x-www-form-urlencoded"}
        request = RequestUtil()
        result = request.request(url, "post", param=data, headers=headers)
        self.assertEqual(result["code"],0,"业务状态不正确")
