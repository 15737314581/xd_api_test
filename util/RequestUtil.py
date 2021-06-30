import requests

"""
工具类封装
"""


class RequestUtil(object):
    def __init__(self):
        pass

    def request(self, url, method, headers=None, param=None, content_type=None):
        """
        通用请求工具类
        @param url:
        @param method:
        @param headers:
        @param param:
        @param content_type:
        @return:
        """

        try:
            if method == "get":
                response = requests.get(url=url, headers=headers, params=param).json()
                return response
            elif method == "post":
                if content_type == "application/json":
                    response = requests.post(url=url, headers=headers, json=param).json()
                    return response
                else:
                    response = requests.post(url=url, headers=headers, data=param).json()
                    return response
            else:
                print("http method not allowed")
        except Exception as e:
            print("http请求报错：{0}".format(e))


if __name__ == '__main__':
    url = "https://api.xdclass.net/pub/api/v1/web/all_category"
    data={"video_id": 61}
    r = RequestUtil()
    result = r.request(url, "get", param=data)
    print(result)