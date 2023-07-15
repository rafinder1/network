
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('profile/<str:name>', views.profile, name='profile'),
    path('fol_posts', views.fol_posts, name='fol_posts'),
    path('compose_post', views.compose_post, name='compose_post'),
    path('profile/<str:name>/follow', views.follow, name='follow'),
    path('profile/is_follow/<str:name>', views.is_follow, name='is_follow'),
    path('profile/count/<str:name>', views.count, name='count'),
    path('edited_post/<int:post_id>', views.edited_post, name='edited_post'),
    path('likes/<int:post_id>', views.likes, name='likes'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
