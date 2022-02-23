import random
from django.core.mail import send_mail


from .models import EmailVerifyRecord
from Zhicheng.settings import EMAIL_FROM


def send_register_email(email,send_type="register"):#参数含义：email将要发送的邮箱地址，type发送邮件的当下情
    email_record = EmailVerifyRecord()
    code = random_str()#随机验证码
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()#将邮箱验证的信息（邮箱号，验证码，验证类型）存入到数据库，为之后用户填写验证码后台做验证的时候使用

    #定义邮件内容
    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "激活链接"
        email_body = "请点击下面的激活链接：http://127.0.0.1:8000/index/active/"+str(code)
        send_status =  send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            return code

    elif send_type == "forget":
        email_title = "密码重置链接"
        email_body = "请点击下面的密码重置链接：http://127.0.0.1:8000/index/reset/"+str(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            return code

    # if send_type == "update":
    #     email_title = "重置邮箱激活验证码"
    #     email_body = "你的邮箱激活验证码为：{0}".format(code)
    #
    #     send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    #     if send_status:
    #         pass


def random_str():
    number = random.randint(100000,999999)
    string = str(number)
    return string
