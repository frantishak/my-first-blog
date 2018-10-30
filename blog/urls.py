from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views


from blog.views import PostViewSet

class BlogRouter(DefaultRouter):
    def get_method_map(self, viewset, method_map):
        map= super(BlogRouter, self).get_method_map(viewset, method_map)
        if 'put' in map and 'post' is not map:
            map['post'] = map ['put']
        return  map

router = BlogRouter()
router.register('posts', PostViewSet, basename='post')
urlpatterns= router.urls



#urlpatterns = [
#    url(r'^$', views.PostListView.as_view(), name='post_list'),
#    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailsView.as_view(), name='post_detail'),
#    url(r'^post/new/$', views.PostNewView.as_view(), name='post_new'),
#    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.PostEditView.as_view(), name='post_edit'),
#]
