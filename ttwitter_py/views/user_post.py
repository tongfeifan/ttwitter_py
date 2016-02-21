from django.views.generic import View, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from ..controller import FollowUserPosts

class Follow_Post(View):
    @method_decorator(login_required)
    def get(self, request, user_name):
        page = request.GET.get('page', 1)
        follow_user_posts = FollowUserPosts(user_name)
        follow_user_posts.set_user_post_list(page)
        total_num = follow_user_posts.total_num
        page_size = follow_user_posts.page_size
        post_list = [{'user_name': each_post.user_name} for each_post in follow_user_posts.user_post_list]
        result = {
            'total_num': total_num,
            'page_size': page_size,
            'page': page,
            'post_list': post_list
        }
        return JsonResponse(data=result)

