from django.contrib.auth.views import LogoutView
from django.urls import path
from users.views import UserLoginView, UserRegisterView, UserView


urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('', UserView.as_view(), name='user'),
]