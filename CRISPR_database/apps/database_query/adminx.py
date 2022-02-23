# import xadmin
# from apps.database_query.models import *
# from xadmin import views
#
#
# class BaseSetting(object):
#     enable_themes = True
#     use_bootswatch = True
#
#
# class GlobaSettings(object):
#     site_title = 'CRISPR Query Admin System'
#     site_footer = 'CRISPR'
#     menu_style = 'accordion'
#
#
# class CRISPR_DATABASEAdmin(object):
#     list_display = ['CRISPR','CRIAPR_name','PI','CRISPR_type','PAM']
#     search_field = ['CRISPR','CRIAPR_name','PI','CRISPR_type','PAM']
#     list_filter = ['CRISPR','CRIAPR_name','PI','CRISPR_type','PAM']
#     list_editable = ['CRISPR','CRIAPR_name','PI','CRISPR_type','PAM']
#
#
#
# #对数据表进行注册
# xadmin.site.register(CRISPR_DATABASE,CRISPR_DATABASEAdmin)
# xadmin.site.register(views.BaseAdminView,BaseSetting)
# xadmin.site.register(views.CommAdminView,GlobaSettings)