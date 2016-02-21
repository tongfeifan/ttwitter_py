from django.conf.urls import url
from django.contrib.auth.views import login

from .views.authentic import Login
from .views.user_post import Follow_Post


urlpatterns = [
    url(r'accounts/login/$', Login.as_view()),
    url(r'u/(?P<user_name>\w+)/', Follow_Post.as_view())
]