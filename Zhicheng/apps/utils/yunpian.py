import json
import requests


class YunPian(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, identifying, mobile):
        parmas = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【刘珂伶】您的验证码是{identifying}".format(identifying=identifying)
        }

        response = requests.post(self.single_send_url, data=parmas)
        re_dict = json.loads(response.text)
        return re_dict


if __name__ == "__main__":
    yun_pian = YunPian("7d850770e04e8ba10d9a93f4b8f77528")
    yun_pian.send_sms("2018", "18328020353")