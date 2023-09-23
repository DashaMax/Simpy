from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import (UserBlogsView, UserBookshelfView, UserEditView,
                         UserLoginView, UserPasswordResetCompleteView,
                         UserPasswordResetConfirmView,
                         UserPasswordResetDoneView, UserPasswordResetView,
                         UserQuotesView, UserRegisterView, UserView)


urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),

    path('password_reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('<slug:user_slug>/', UserView.as_view(), name='user'),
    path('<slug:user_slug>/edit/', UserEditView.as_view(), name='edit'),
    path('<slug:user_slug>/bookshelf/', UserBookshelfView.as_view(), name='bookshelf'),
    path('<slug:user_slug>/user-blogs/', UserBlogsView.as_view(), name='user-blogs'),
    path('<slug:user_slug>/user-quotes/', UserQuotesView.as_view(), name='user-quotes'),
]