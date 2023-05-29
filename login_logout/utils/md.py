from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect

class PermissionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path_info == "/login/":
            return
        user_info = request.session.get("user_info")

        if user_info:
            request.unicom_userid = user_info['id']
            request.unicom_username = user_info['userName']
            return

        return redirect('/login/')

    def process_response(self, request, response):
        return response