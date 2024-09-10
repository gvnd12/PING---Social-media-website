from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import *


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('admin/', admin_login, name='adminlogin'),
    path('adminlogout/', admin_logout, name='adminlogout'),
    path('adminhome/', admin_home, name='adminhome'),
    path('users/', users, name='users'),
    path('createuser/', create_user, name='createuser'),
    path('createpost/', create_post, name='createpost'),
    path('posts/<int:user_id>', posts, name='posts'),
    path('adminfollowers/<int:user_id>', followers, name='follower'),
    path('adminfollowing/<int:user_id>', following, name='following'),
    path('deleteuser/<int:user_id>', user_delete, name='user_delete'),
    path('deletepost/<int:post_id>', post_delete, name='post_delete')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)