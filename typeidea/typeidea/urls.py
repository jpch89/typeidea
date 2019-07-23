import xadmin
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.sitemaps import views as sitemap_views
from rest_framework.routers import DefaultRouter

from blog.apis import PostViewSet
# from blog.apis import PostList, post_list
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from blog.views import (AuthorView, CategoryView, IndexView, PostDetailView,
                        SearchView, TagView)
from comment.views import CommentView
from config.views import LinkListView

from .autocomplete import CategoryAutocomplete, TagAutocomplete

router = DefaultRouter()
router.register(r'post', PostViewSet, base_name='api-post')

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<category_id>\d+)/$',
        CategoryView.as_view(),
        name='category-list'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag-list'),
    url(r'^post/(?P<post_id>\d+).html$',
        PostDetailView.as_view(),
        name='post-detail'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^author/(?P<owner_id>\d+)/$', AuthorView.as_view(), name='author'),
    url(r'^links/$', LinkListView.as_view(), name='links'),
    url(r'^comment/$', CommentView.as_view(), name='comment'),
    url(r'^rss|feed/', LatestPostFeed(), name='rss'),
    url(r'^category-autocomplete/$', CategoryAutocomplete.as_view(), name='category-autocomplete'),
    url(r'^tag-autocomplete/$', TagAutocomplete.as_view(), name='tag-autocomplete'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^sitemap\.xml$', sitemap_views.sitemap, {'sitemaps': {'posts': PostSitemap}}),
    url(r'^admin/', xadmin.site.urls, name='xadmin'),
    # url(r'^api/post/', post_list, name='post-list'),
    # url(r'^api/post/', PostList.as_view(), name='post-list'),
    url(r'^api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
