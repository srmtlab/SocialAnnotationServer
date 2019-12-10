from django.urls import path
from . import views

"""
GETリクエスト
    / : index.htmlの表示
"""

app_name = 'SocialAnnotation'
urlpatterns = [
    # GET request
    path('', views.index, name='index'),
]