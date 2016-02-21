from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, TemplateView
from django.http import HttpResponseRedirect, JsonResponse

from ..models import UserProfile


class Login(TemplateView):
    template_name = "login.html"
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/u/{}/".format(username))
            else:
                form = {
                    'error': True,
                }
                return JsonResponse(data=form)

        else:
            form = {
                'error': True
            }
            return JsonResponse(data=form)


def logout_view(request):
    logout(request)

class Register(View):
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
