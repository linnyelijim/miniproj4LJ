# INF601 - Advanced Programming in Python
# Lindsey Jimenez
# Mini Project 4

from . import views
from django.urls import path


# Contains all app urls
urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('post_detail/', views.post_detail, name='post_detail'),
    path('about/', views.About.as_view(), name='about'),
    path('games/', views.Games.as_view(), name='games'),
    path('contact/', views.contact, name='contact'),
    path('success/', views.success, name='success'),
    path('register/', views.register_request, name="register"),
    path('login/', views.login_request, name="login"),
    path('accounts/logout/', views.logout_request, name="logout"),
    path('password_reset', views.password_reset_request, name="password_reset"),
    path('main/', views.main, name='main'),
    path('add_forum/', views.add_forum, name='add_forum'),
    path('add_discussion/', views.add_discussion, name='add_discussion'),
    path('get_games/', views.GetGames.as_view(template_name='games/get_games.html'), name='Game View'),
    path('profile/', views.profile, name='users_profile'),
]
