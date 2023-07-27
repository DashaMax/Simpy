from django.contrib.auth.views import LogoutView
from django.urls import path
from users.views import UserLoginView, UserRegisterView, UserView, UserEditView, UserBookshelfView, UserBlogsView


urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('<slug:slug>/', UserView.as_view(), name='user'),
    path('<slug:slug>/edit/', UserEditView.as_view(), name='edit'),
    path('<slug:slug>/bookshelf/', UserBookshelfView.as_view(), name='bookshelf'),
    path('<slug:slug>/blogs/', UserBlogsView.as_view(), name='user-blogs'),
]