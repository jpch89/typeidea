from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Post, Category, Tag
from config.models import SideBar


class PostListView(ListView):
    queryset = Post.latest_posts()
    paginate_by = 1
    # 如果不设置此项，在模板中需要使用 object_list 变量
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'sidebars': SideBar.get_all()})
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'
