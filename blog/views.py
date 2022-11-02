from django.views import generic
from .models import Post


# Provides generic list with objects of specified model
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 3


# Provides a detailed view for given object of the model
class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'