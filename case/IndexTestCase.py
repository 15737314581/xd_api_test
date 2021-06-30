#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests
import unittest
from util.RequestUtil import RequestUtil

'''
@Project ：test 
@File    ：IndexTestCase.py
@Author  ：jijianfeng
@Date    ：2021/6/30 下午2:52 
'''
host = "https://api.xdclass.net"


class IndexTestCase(unittest.TestCase):

    def testIndexCategoryList(self):
        """
        首页分类列表
        @return:
        """
        url = host + "/pub/api/v1/web/all_category"
        reqest = RequestUtil()
        result = reqest.request(url, "get")
        self.assertEqual(result["code"], 0, "业务状态不正常")
        self.assertTrue(len(result["data"]) > 0, "分类列表为空")

    def testIndexVideoCard(self):
        """
        首页视频卡片
        @return:
        """
        url = host + "/pub/api/v1/web/index_card"
        reqest = RequestUtil()
        result = reqest.request(url, "get")
        self.assertEqual(result["code"], 0, "业务状态不正常")
        video_card_list = result["data"]
        for card in video_card_list:
            self.assertTrue(len(card["title"]) > 0, "卡片标题为空 id：" + str(card["id"]))


if __name__ == '__main__':
    unittest.main(verbosity=2)
