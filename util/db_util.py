#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pymysql
from config.read_config import *
from warnings import filterwarnings

# 忽略mysql告警
filterwarnings("ignore", category=pymysql.Warning)


class MysqlDb(object):
    readconfig = ReadConfig()
    host = readconfig.get_db("Mysql-Database", "host")
    user = readconfig.get_db("Mysql-Database", "user")
    password = readconfig.get_db("Mysql-Database", "password")
    db = readconfig.get_db("Mysql-Database", "db")

    def __init__(self):
        # 建立数据库连接
        self.connect = pymysql.connect(host=MysqlDb.host, user=MysqlDb.user, password=MysqlDb.password,
                                       database=MysqlDb.db)
        #  使用cursor方法操作游标，得到一个可以操作sql语句，并且操作结果作为字典返回的游标
        self.cursor = self.connect.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):
        # 关闭游标
        self.cursor.close()
        # 关闭连接
        self.connect.close()

    def query(self, sql, state="all"):
        """
        查询
        @param sql:
        @param state: 默认查询全部
        @return:
        """
        self.cursor.execute(sql)
        if state == "all":
            data = self.cursor.fetchall()
        else:
            data = self.cursor.fetchone()
        return data

    def execute(self, sql):
        """
        新增，删除，修改
        @param sql:
        @return:
        """
        try:
            rows = self.cursor.execute(sql)
            self.connect.commit()
            return rows
        except Exception as e:
            print(e)
            self.connect.rollback()


if __name__ == '__main__':
    test = MysqlDb()
    # sql = "select * from `case` "
    sql = "insert into `case` (app) values ('啊哈哈')"
    data = test.execute(sql)
    print(data)
