import xadmin

from .models import Label,Article,Comment,Replay


class LabelAdmin(object):
    list_display = ['label', 'add_time']
    list_filter = ['label', 'add_time']
    search_filter = ['label']


class ArticleAdmin(object):
    list_display = ['user','title','city','label','content','file','click_nums','fav_nums','update_time','add_time']
    list_filter = ['user__username','title','city','label__label','content','file','click_nums','fav_nums','update_time','add_time']
    search_filter = ['user','title','city','label','content','file','click_nums','fav_nums']
    style_fields = {"content": "ueditor"}


class CommentAdmin(object):
    list_display = ['commenter','article','comment_content','fav_nums','accept_nums','add_time']
    list_filter = ['commenter__username','article__title','comment_content','fav_nums','accept_nums','add_time']
    search_filter = ['commenter','article','comment_content','fav_nums','accept_nums']


class ReplayAdmin(object):
    list_display = ['comment','replay_contenter','replay_content','add_time']
    list_filter = ['comment__comment_content','replay_contenter__username','replay_content','add_time']
    search_filter = ['comment','replay_contenter','replay_content']

xadmin.site.register(Label,LabelAdmin)
xadmin.site.register(Article,ArticleAdmin)
xadmin.site.register(Comment,CommentAdmin)
xadmin.site.register(Replay,ReplayAdmin)