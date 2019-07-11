"""
查询某个对象的变更记录
"""
from django.contrib.admin.models import LogEntry
from django.contrib.admin.options import get_content_type_for_model
from blog.models import Post


post = Post.objects.get(id=1)
log_entries = LogEntry.objects.filter(
    content_type_id=get_content_type_for_model(post).pk,
    object_id=post.id,
)
