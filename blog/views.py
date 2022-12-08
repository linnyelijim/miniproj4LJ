# INF601 - Advanced Programming in Python
# Lindsey Jimenez
# Mini Project 4
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .services import get_games
from .forms import CommentForm, ContactForm, NewUserForm, CreateInForum, CreateInDiscussion, UserForm, ProfileForm
from .models import Post, Forum
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import generic
import requests


# Provides generic list with objects of specified model
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'home/index.html'
    paginate_by = 3


# Provides a detailed view for given object of the model
def post_detail(request):
    template_name = 'home/post_detail.html'
    post = get_object_or_404(Post)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})


# Accepts contact inquiry
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'subject': form.cleaned_data['subject'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, 'admin@example.com', ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')

    form = ContactForm()
    return render(request, 'contact/contact.html', {'form': form,
                                                    })


# Creates success response
def success(request):
    return HttpResponse('Success! Thank you for your message.')


# Will contain about page details if needed
class About(generic.TemplateView):
    template_name = "about/about.html"


# Will contain games page details if needed
class Games(generic.TemplateView):
    template_name = "games/games.html"


# Allows user to register an account
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="accounts/register.html", context={"register_form": form})


# Allows user to login
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="accounts/login.html", context={"login_form": form})


# Allows user to logout
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "accounts/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="accounts/password_reset.html",
                  context={"password_reset_form": password_reset_form})


@login_required
def profile(request):
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    return render(request=request, template_name="users/profile.html",
                  context={"user": request.user, "user_form": user_form, "profile_form": profile_form})


def main(request):
    forums = Forum.objects.all()
    count = forums.count()
    discussions = []
    for i in forums:
        discussions.append(i.discussion_set.all())

    context = {'forums': forums,
               'count': count,
               'discussions': discussions}
    return render(request, 'forum/main.html', context)


def add_forum(request):
    thread = CreateInForum()
    if request.method == 'POST':
        thread = CreateInForum(request.POST)
        if thread.is_valid():
            thread.save()
            return redirect('forum/main.html')
    context = {'thread': thread}
    return render(request, 'forum/add_forum.html', context)


def add_discussion(request):
    forum = CreateInDiscussion()
    if request.method == 'POST':
        forum = CreateInDiscussion(request.POST)
        if forum.is_valid():
            forum.save()
            return redirect('forum/main.html')
    context = {'forum': forum}
    return render(request, 'forum/add_discussion.html', context)


class GetGames(TemplateView):
    template_name = 'games/get_games.html'

