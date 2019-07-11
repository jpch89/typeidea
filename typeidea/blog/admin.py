from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site


class PostInline(admin.TabularInline):  # StackedInline 样式不同
    fields = ('title', 'desc')
    extra = 1  # 额外多几行，也可以为 0
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(admin.ModelAdmin):
    # 展示页面
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')

    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'

    # 编辑页面
    fields = ('name', 'status', 'is_nav')
    # 不能写成：inlines = ['PostInline', ]
    inlines = [PostInline, ]

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Tag, site=custom_site)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户分类"""
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(
            owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


# 下面是 SSO 的实现：单点登录（Single Sign-On）
# import requests

# from django.contrib.auth import get_permission_codename

# PERMISSION_API = 'http://permission.sso.com/has_per?user={}&per_code={}'


@admin.register(Post, site=custom_site)
class PostAdmin(admin.ModelAdmin):
    # 单点登录
    """
    def has_add_permission(self, request):
        opts = self.opts
        codename = get_permission_codename('add', opts)
        perm_code = '%s.%s' % (opts.app_label, codename)
        resp = requests.get(PERMISSION_API.format(request.user.name, perm_code))
        if resp.status_code == 200:
            return True
        else:
            return False
    """

    form = PostAdminForm
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operator',
    ]
    # 这样并不能禁用编辑
    # list_display_links = []
    # 这样才行
    list_display_links = None

    # list_filter = ['category', ]
    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']

    actions_on_top = True
    acitons_on_bottom = True

    # 编辑页面
    save_on_top = True
    exclude = ('owner', )
    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('collapse', ),
            'fields': ('tag', )
        }),
    )
    filter_horizontal = ('tag', )
    # 或者是下面的
    filter_vertical = ('tag', )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id, ))
        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(owner=request.user)

    class Media:
        css = {
            'all': ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css', ),
        }
        js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )
