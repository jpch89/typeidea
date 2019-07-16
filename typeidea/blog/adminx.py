from django.urls import reverse
from django.utils.html import format_html
import xadmin
from xadmin.filters import manager
from xadmin.filters import RelatedFieldListFilter
from xadmin.layout import Row, Fieldset, Container

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea.base_admin import BaseOwnerAdmin


class PostInline:
    form_layout = (
        Container(
            Row('title', 'desc'),
        )
    )
    extra = 1  # 控制额外多几个
    model = Post


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    # 展示页面
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')

    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'

    # 编辑页面
    fields = ('name', 'status', 'is_nav')


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(RelatedFieldListFilter):
    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, parames, model, model_admin, field_path)
        # 重新获取 lookup_choices，根据 owner 过滤
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')


manager.register(CategoryOwnerFilter, take_priority=True)


class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator',
    ]

    list_display_links = []
    list_filter = ['category', ]
    list_filter = [CategoryOwnerFilter, ]
    search_fields = ['title', 'category__name']

    actions_on_top = True
    acitons_on_bottom = True

    # 编辑页面
    save_on_top = True
    # 没有这一句好像也可以
    # exclude = ['owner']

    form_layout = (
        Fieldset(
            '基础信息',
            Row('title', 'category'),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'content',
        )
    )

    filter_vertical = ('tag', )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:blog_post_change', args=(obj.id, ))
            # self.model_admin_url('change', obj.id)
        )
    operator.short_description = '操作'

    # @property
    # def media(self):
    #     # xadmin 基于 Bootstrap，引入会导致页面样式冲突，这里只做演示
    #     media = super().Media
    #     media.add_js(['https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js'])
    #     media.add_css({
    #         'all': ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/boostrap.min.css'),
    #     })
    #     return media
