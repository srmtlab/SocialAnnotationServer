from django.http import HttpResponseNotAllowed
from django.shortcuts import render


def index(request):
    if request.method == "GET":
        return render(request, 'SocialAnnotation/index.html')
    else:
        message = request.method + "は許可されていないメソッドタイプです"
        return HttpResponseNotAllowed(['GET'], message)


