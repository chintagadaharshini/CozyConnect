from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('feed/', views.feed_view, name='feed'),
    path('create/', views.create_post_view, name='create_post'),
    path('like/<int:post_id>/', views.like_post_view, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment_view, name='add_comment'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/edit/me/', views.edit_profile_view, name='edit_profile'),
    path('follow/<str:username>/', views.follow_view, name='follow'),
]