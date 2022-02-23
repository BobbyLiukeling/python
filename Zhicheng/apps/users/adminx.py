from .models import UserProfile, EmailVerifyRecord
import xadmin


class UserProfileAdmin(object):
    list_display = ['username','city','mobile','email','birthday','gender','image','profession','rand','credit','add_time']
    list_filter = ['username','city','mobile','email','birthday','gender','image','profession','rand','credit','add_time']
    search_filter = ['username','city','mobile','email','birthday','gender','image','profession','rand','credit']


class EmailVerifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time']
    list_filter = ['code','email','send_type','send_time']
    search_filter = ['code','email','send_type']

#userprofile在xadmin中就已经默认注册过了，这里就不再注册了

xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)



