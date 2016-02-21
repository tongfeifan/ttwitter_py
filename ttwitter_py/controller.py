from django.shortcuts import render

from .models import UserPost, UserProfile
# Create your views here.


class FollowUserPosts(object):
    """
    PO文列表
    """
    def __init__(self, user_name=None, page_size=10):
        self.user_name = user_name
        self.user_post_list = []
        self.total_num = 0
        self.page_size = page_size

    def set_user_post_list(self, page):
        """
        为PO文列表对象生成内容(分页)

        :param page: 页码
        :return:
        """
        page += 1
        follow_list = self._get_follow_list()
        user_post_query_set = self._get_user_posts(follow_list)
        self.total_num = user_post_query_set.count()
        self.user_post_list = [{"nick_name": each_post.user__nickname, "content": each_post.content,
                                "post_date": each_post.creation_date}
                               for each_post in user_post_query_set[page * self.page_size: (page + 1) * self.page_size]]


    def _get_user_posts(self, user_names):
        user_post_query_set = UserPost.objects.filter(user__username__in=user_names).order_by("-creation_date")
        return user_post_query_set

    def _get_follow_list(self):
        if not self.user_name:
            raise ValueError("user id should be initialize before call this method")
        user_follow_query_set = UserProfile.objects.filter(followed_by__username=self.user_name).all()
        follow_list = [each_user.username for each_user in user_follow_query_set]
        return follow_list


class UserBaseInfo(object):
    def __init__(self, user_name, nick_name):
        self.user_name = user_name
        self.nick_name = nick_name


class UserInfoList(object):
    """
    用户信息列表基类
    """
    def __init__(self):
        self.user_list = []
        self.total_num = 0
        self.page = 0
        self.page_size = 10
        self.num = 0


class FollowInfoList(UserInfoList):
    def followed_by(self, user_name, page_size=None, page=None):
        """
        获得关注列表的分页结果

        :param user_name:
        :param page_size: (optional)
        :param page: (optional)
        :return:
        """
        if not UserProfile.objects.filter(username=user_name).exists():
            raise ValueError('This user id is not exist')

        if page_size:
            self.page_size = page_size
        if page:
            self.page = page

        user_profile_query_set = UserProfile.objects.filter(followed_by__username=user_name).all()
        self.num = user_profile_query_set.count()
        self.user_list = [UserBaseInfo(user.username, user.nickname)
                          for user in user_profile_query_set[self.page * self.page_size :(self.page + 1) * self.page_size]]
        return self


class FollowerInfoList(UserInfoList):
    def follow_to(self, user_name, page_size=None, page=None):
        """
        获得跟随者列表的分页结果

        :param user_name:
        :param page_size: (optional)
        :param page: (optional)
        :return:
        """
        if not UserProfile.objects.filter(username=user_name).exists():
            raise ValueError('This user id is not exist')

        if page_size:
            self.page_size = page_size
        if page:
            self.page = page

        user_profile_query_set = UserProfile.objects.filter(follows=user_name).all()
        self.num = user_profile_query_set.count()
        self.user_list = [UserBaseInfo(user.username, user.nickname)
                          for user in user_profile_query_set[self.page: self.page + self.page_size]]
        return self
