from django import template

from comment.forms import CommentForm
from comment.models import Comment


register = template.Library()


# 个人理解这个标签做了两件事：
# 1. 添加 context 数据
# 2. 用添加好的 context 数据渲染 comment/block.html，将其嵌入模板标签的位置
# 另外，在使用该标签的时候，需要传入 target
@register.inclusion_tag('comment/block.html')
def comment_block(target):
    return {
        'target': target,
        'comment_form': CommentForm(),
        'comment_list': Comment.get_by_target(target),
    }