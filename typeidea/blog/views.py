from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Post, Category, Tag
from config.models import SideBar


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'sidebars': SideBar.get_all()})
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    # 如果不设置此项，在模板中需要使用 object_list 变量
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({'category': category})
        return context

    def get_queryset(self):
        """重写 queryset，根据分类过滤"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({'tag': tag})
        return context

    def get_queryset(self):
        """重写 queryset，根据标签过滤"""
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag_id=tag_id)


class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    # 在模板中需要使用的上下文名字
    context_object_name = 'post'
    # 用于接收来自 url 的主键，根据这个主键进行查询
    pk_url_kwarg = 'post_id'


class SearchView(IndexView):
    def get_context_data(self):
        context = super().get_context_data()
        context.update({'keyword': self.request.GET.get('keyword', '')})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword', '')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))
