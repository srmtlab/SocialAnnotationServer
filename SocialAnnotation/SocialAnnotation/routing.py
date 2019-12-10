from django.urls import path
from . import consumers

"""
WebSocketリクエスト
    ws/ : WebSocketを用いた，アノテーションの編集(追加・削除・編集)
"""

websocket_urlpatterns = [
    path('ws/', consumers.SocialAnnotationConsumer, name='websocket_index'),
]