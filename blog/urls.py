from . import views
from django.urls import path

# Homepage url, slug url
urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('post_detail/', views.post_detail, name='post_detail'),
    path('about/', views.about, name='about'),
    path('games/', views.games, name='games'),
    path('contact/', views.contact, name='contact'),
    path('success/', views.success, name='success'),
]
