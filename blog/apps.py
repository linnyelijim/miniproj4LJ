# INF601 - Advanced Programming in Python
# Lindsey Jimenez
# Mini Project 4

from django.apps import AppConfig


# Configures blog app
class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
