from . import views
from django.urls import path

# Homepage url, slug url
urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('post_detail/', views.post_detail, name='post_detail'),
    path('about/', views.About.as_view(), name='about'),
    path('games/', views.Games.as_view(), name='games'),
    path('contact/', views.contact, name='contact'),
    path('success/', views.success, name='success'),
]
