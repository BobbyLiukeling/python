import pdb
import re
def jwt_response_payload_handler(token, user=None, request=None):#返回登录信息
    '''

    :param token:
    :param user:
    :param request:
    :return:
    '''
    # if user.image.path:
    #     image = user.image.path
    # else:
    #     image = ''

    try:
        image = user.image.path
        image = 'http://127.0.0.1:8000'+image[image.index('media')+len('media'):len(image)].replace('\\','/')
    except Exception:
        image = ''


    return {
        'token': token,
        # 'user': UserSerializer(user, context={'request': request}).data
        'id':user.id,
        'is_superuser':user.is_superuser,
        'username':user.username,
        'mobile':user.mobile,
        'email':user.email,
        'city':user.city,
        'rand':user.rand,
        'credit':user.credit,
        'profession':user.profession,
        'image':image,
        'sign':user.sign,
    }


from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class CustomBackend(ModelBackend):
    """
    自定义用户验证规则
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因
            # 后期可以添加邮箱验证
            user = User.objects.get(
                Q(username=username) | Q(mobile=username))
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self,
            # raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None
