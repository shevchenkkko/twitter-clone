from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name='home'),
    path('profile_list/', profile_list, name='profile_list'),
    path('profile/<int:pk>', profile , name='profile'),
    path('profile/followers/<int:pk>', profile_followers , name='profile_followers'),
    path('profile/following/<int:pk>', profile_following , name='profile_following'),
    path('add_tweet/', add_tweet , name='add_tweet'),
    path('login/', login_user , name='login'),
    path('register/', register_user , name='register'),
    path('logout/', logout_user , name='logout'),
    path('update_user/', update_user , name='update_user'),
    path('like_post/<int:pk>', like_post , name='like_post'),
    path('like_comment/<int:pk>', like_comment , name='like_comment'),
    path('follow/<int:pk>', follow , name='follow'),
    path('unfollow/<int:pk>', unfollow , name='unfollow'),
    path('delete_tweet/<int:pk>', delete_tweet , name='delete_tweet'),
    path('delete_comment/<int:pk>', delete_comment , name='delete_comment'),
    path('edit_tweet/<int:pk>', edit_tweet , name='edit_tweet'),
    path('edit_comment/<int:pk>', edit_comment , name='edit_comment'),
    path('comment/<int:pk>', add_comment , name='comment'),
]
