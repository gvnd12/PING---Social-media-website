from django.contrib import admin
from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', user_login, name='login'),
    path('register/', user_registration, name='register'),
    path('edit/<int:userid>/', edit_profile, name='edit'),
    path('logout/', user_logout, name='logout'),
    path('post/', user_post, name='post'),
    path('profile/', profile, name='profile'),
    path('notifications/', view_notifications, name='notifications'),
    path('like/<int:post_id>', like, name='like'),
    path('followers/<int:user_id>', user_followers, name='follower'),
    path('following/<int:user_id>', user_following, name='following'),
    path('search/', user_search, name='search'),
    path('searchprofile/<int:user_id>', searchprofile, name='searchprofile'),
    path('follow_unfollow/<int:user_id>', follow_unfollow, name='follow_unfollow'),
    path('feed/', feed, name='feed'),
    path('viewcomments/<int:post_id>', view_comments, name='viewcomments'),
    path('comment/<int:post_id>', user_comment, name='comment'),
    path('msgsend/<int:receiver_id>', msgsend, name='msgsend'),
    path('ping/', user_ping, name='ping'),
    path('pingreply/<int:ping_id>', ping_reply, name='pingreply'),
    path('view_ping_reply/<int:ping_id>', view_ping_reply, name='viewpingreply'),
    path('userdeletepost/<int:post_id>', userdeletepost, name='userdeletepost')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)