# coding = utf-8
import json
import time
from datetime import datetime

from util.db_util import MysqlDb
from util.request_util import RequestUtil
from util.send_mail import SendMail

"""
八大骨架方法
"""


class XdclassTestCase:
    def loadAllCaseByApp(self, app):
        """
        根据app加载所有用例
        @param app:
        @return:
        """
        my_db = MysqlDb()
        sql = "select * from `case` where app = '{0}'".format(app)
        results = my_db.query(sql)
        return results

    def findCaseByCaseId(self, case_id):
        """
        根据id查找对应用例
        @param id:
        @return:
        """
        my_db = MysqlDb()
        sql = "select * from `case` where id = '{0}'".format(case_id)
        results = my_db.query(sql, state="one")
        return results

    def loadConfigByAppAndKey(self, app, key):
        """
        根据app和key加载配置
        @param app:
        @param key:
        @return:
        """
        my_db = MysqlDb()
        sql = "select * from `config` where app = '{0}' and dict_key = '{1}'".format(app, key)
        results = my_db.query(sql, state="one")
        return results

    def updateResultByCaseId(self, response, is_pass, msg, case_id):
        """
        根据用例id，更新响应内容和测试内容
        @param response:
        @param is_pass:
        @param msg:
        @param case_id:
        @return:
        """
        my_db = MysqlDb()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(current_time)
        if is_pass:
            sql = "update `case` set response = '{0}',pass='{1}',update_time='{2}',msg='{3}' where id={4}".format("",
                                                                                                                  is_pass,
                                                                                                                  current_time,
                                                                                                                  msg,
                                                                                                                  case_id)
        else:
            sql = "update `case` set response = \"{0}\",pass='{1}',update_time='{2}',msg='{3}' where id={4}".format(
                str(response),
                is_pass,
                current_time,
                msg,
                case_id)
        print(sql)
        rows = my_db.execute(sql)
        print(rows)

    def runAllCase(self, app):
        """
        执行全部用例的入口
        @param app:
        @return:
        """
        # 获取接口域名配置
        api_host_obj = self.loadConfigByAppAndKey(app, "host")
        # 获取全部用例
        results = self.loadAllCaseByApp(app)
        # 遍历用例集
        for case in results:
            print(case)
            if case["run"] == "yes":
                try:
                    # 执行单个用例
                    response = self.runCase(case, api_host_obj)
                    # 响应断言
                    assert_msg = self.assertResponse(case, response)
                    # 更新结果存储数据库
                    rows = self.updateResultByCaseId(response, assert_msg["is_pass"], assert_msg["msg"], case["id"])
                    print("更新结果：rows={0}".format(str(rows)))
                except Exception as e:
                    print("用例id：{0} 用例标题：{1} 执行报错：{2}".format(case["id"], case["title"], e))

        # 发送测试报告
        self.sendTsetReport(app)

    def runCase(self, case, api_host_obj):
        """
        执行单个用例
        @param case:
        @param api_host_obj:
        @return:
        """
        headers = json.loads(case["headers"])
        body = json.loads(case["request_body"])
        method = case["method"]
        req_url = api_host_obj["dict_value"] + case["url"]
        # 判断是否有前置条件
        if case["pre_case_id"] > -1:
            pre_case = self.findCaseByCaseId(case["pre_case_id"])
            # 递归调用
            pre_response = self.runCase(pre_case, api_host_obj)
            # 前置条件断言
            pre_assert_msg = self.assertResponse(pre_case, pre_response)
            if not pre_assert_msg["is_pass"]:
                # 前置条件不通过直接返回
                pre_response["msg"] = "前置条件不通过：" + pre_response["msg"]
                return pre_response
            # 判断需要case的前置条件是哪个字段
            pre_fields = json.loads(case["pre_fields"])
            for pre_field in pre_fields:
                print(pre_field)
                if pre_field["scope"] == "header":
                    # 遍历headers，替换对应的字段值，即寻找同名字段
                    for header in headers:
                        field_name = pre_field["field"]
                        if header == field_name:
                            field_value = pre_response["data"][field_name]
                            headers[field_name] = field_value
                elif pre_field["scope"] == "body":
                    for r_body in body:
                        field_name = pre_field["field"]
                        if r_body == field_name:
                            field_value = pre_response["data"][field_name]
                            body[field_name] = field_value

        print(headers)
        requset = RequestUtil()
        response = requset.request(req_url, method, headers=headers, param=body)
        return response

    def assertResponse(self, case, response):
        """
        断言响应内容，更新用例执行情况
        @param case:
        @param response:
        @return:
        """
        assert_type = case["assert_type"]
        expect_result = case["expect_result"]
        is_pass = False
        # 判断断言类型
        if assert_type == "code":
            if response["code"] == int(expect_result):
                is_pass = True
                print("用例执行通过")
            else:
                is_pass = False
                print("用例执行不通过")
        elif assert_type == "data_json_array":
            response_data = response["data"]
            if response_data is not None and isinstance(response_data, list) and len(response_data) > int(
                    expect_result):
                is_pass = True
                print("用例执行通过")
            else:
                is_pass = False
                print("用例执行不通过")
        elif assert_type == "data_json":
            response_data = response["data"]
            if response_data is not None and isinstance(response_data, dict) and len(response_data) > int(
                    expect_result):
                is_pass = True
                print("用例执行通过")
            else:
                is_pass = False
                print("用例执行不通过")
        # 拼装信息
        msg = "模块:{0}, 标题:{1}, 断言类型:{2}, 响应:{3}".format(case["app"], case["title"], assert_type, response["msg"])
        assert_msg = {"is_pass": is_pass, "msg": msg}
        return assert_msg

    def sendTsetReport(self, app):
        """
        发送邮件，测试报告
        @param app:
        @return:
        """
        results = self.loadAllCaseByApp(app)
        mail_title = self.loadConfigByAppAndKey(app,"mail_title")["dict_value"]
        content = """
        <html><body>
        <h4>{0} 接⼝口测试报告:</h4> 
        <table border="1">
        <tr>
            <th>编号</th>
            <th>模块</th>
            <th>标题</th> 
            <th>是否通过</th> 
            <th>备注</th> 
            <th>响应</th>
        </tr>
        {1}
        </table></body></html>
        """
        template = ""
        for case in results:
            template += "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td></tr>".format(
                case["id"],
                case["module"],
                case["title"],
                case["pass"],
                case["msg"],
                case["response"])
        current_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        mail_content = content.format(current_time, template)
        mail_host = self.loadConfigByAppAndKey(app,"mail_host")["dict_value"]
        mail_sender = self.loadConfigByAppAndKey(app,"mail_sender")["dict_value"]
        mail_auth_code = self.loadConfigByAppAndKey(app,"mail_auth_code")["dict_value"]
        mail_receivers = self.loadConfigByAppAndKey(app,"mail_receivers")["dict_value"].split(",")
        mail = SendMail(mail_host)
        mail.send(mail_title,mail_content,mail_sender,mail_auth_code,mail_receivers)



if __name__ == '__main__':
    # print("main")
    # test = xdclassTestCase()
    # # results = test.loadAllCaseByApp("小滴课堂")
    # results = test.findCaseByCaseId(1)
    # print(results)
    test = XdclassTestCase()
    test.runAllCase("小滴课堂")
