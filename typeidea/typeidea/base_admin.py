from django.contrib import admin


# class BaseOwnerAdmin(admin.ModelAdmin):
class BaseOwnerAdmin(object):
    """
    1. 用来自动补充文章、分类、标签、侧边栏、友链这些 Model 的 owner 字段
    2. 用来针对 queryset 过滤当前用户的数据
    """
    # 对应于 fields，是不想显示的字段
    exclude = ('owner', )

    def get_list_queryset(self):
        request = self.request
        qs = super().get_list_queryset()
        return qs.filter(owner=request.user)

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.filter(owner=request.user)

    def save_models(self):
        self.new_obj.owner = self.request.user
        return super().save_models()

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super().save_model(request, obj, form, change)
