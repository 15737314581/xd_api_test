# coding = utf-8
import requests

# response = requests.get("https://api.xdclass.net/pub/api/v1/web/all_category")

# data = {"video_id": 61}
# response = requests.get("https://api.xdclass.net/pub/api/v1/web/video_detail", data)

data = {"phone": "15737314581", "pwd": "13519553700jjf1"}
response = requests.post("https://api.xdclass.net/pub/api/v1/web/web_login", data=data)
print(response.status_code)
print(response.text)
