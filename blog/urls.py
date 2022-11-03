from . import views
from django.urls import path, re_path

# Homepage url, slug url
urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('post_detail/', views.post_detail, name='post_detail'),
    path('about/', views.contact, name='about'),
    path('games/', views.contact, name='games'),
    path('contact/', views.contact, name='contact'),
    path('success/', views.success, name='success'),
]
