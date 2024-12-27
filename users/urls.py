from django.urls import path
from users.views import RegisterAPIView, LoginAPIView

urlpatterns= [
    path('register/', RegisterAPIView.as_view(), name='user-register'),
    path('login/', LoginAPIView.as_view(), name='user-login'),
]