# coding = utf-8
import smtplib
from email.mime.text import MIMEText


class SendMail(object):
    def __init__(self, mail_host):
        self.mail_host = mail_host

    def send(self, title, content, sender, auth_code, receivers):
        message = MIMEText(content, "html", "utf-8")
        message["From"] = "{}".format(sender)
        message["To"] = ",".join(receivers)
        message["Subject"] = title
        try:
            smtp_ssl = smtplib.SMTP_SSL(self.mail_host, 465)  # 启用ssl发信，端口一般为465
            smtp_ssl.login(sender, auth_code)  # 登录
            smtp_ssl.sendmail(sender,receivers,message.as_string())
            print("Mail 发送成功")


        except Exception as e:
            print(e)


if __name__ == '__main__':
    mail = SendMail("smtp.126.com")
    sender = "jjf15737314581jjf@126.com"
    receivers = ["1065109432@qq.com"]
    title = "接口测试"
    content = """
    小滴课堂 xdclass.net
    <a href = "https://xdclass.net">进入学习</a>
    """
    auth_code = "UTYDBMELVUYBANHD"
    mail.send(title,content,sender,auth_code,receivers)
