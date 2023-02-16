
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Topic, Tag
from .forms import PostForm, CommentForm, LoginForm, SignInForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
# 1. Widok wyświetlający stronę główną.
def index(request):
    topics = Topic.objects.all()
    return render(request, 'templates/index.html', {'topics': topics})
# 2. Widok wyświetlający temat i mogący robić np listę.
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    posts = topic.post_set.all()
    return render(request, 'templates/topic.html', {'topic': topic, 'posts': posts})
# 3. Widok umożliwiający dodawanie nowego posta.
@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.topic_id = request.POST.get('topic_id')
            post.save()
            return redirect('topic', topic_id=post.topic_id)
    else:
        form = PostForm()
    return render(request, 'templates/new_post.html', {'form': form})
# 4. Widok umożliwiający dodawanie nowego komentarza.
@login_required
def new_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post_id = request.POST.get('post_id')
            comment.save()
            return redirect('topic', topic_id=comment.post.topic_id)
    else:
        form = CommentForm()
    return render(request, 'templates/new_comment.html', {'form': form})
# 5. Widok wyświetlający wszystkie tagi.
def tags(request):
    tags = Tag.objects.all()
    return render(request, 'templates/tags.html', {'tags': tags})
# 6. Widok umożliwiający logowanie.
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'templates/registration/login.html', {'form': form, 'invalid': True})
    else:
        form = LoginForm()
    return render(request, 'templates/registration/login.html', {'form': form})
# 7. Widok umożliwiający rejestrację.
def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Hello {username}, welcome back!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = SignInForm()
    return render(request, 'registration/signin.html', {'form': form})
# 8. Widok wyświetlający informacje o autorze strony.
def aboutme(request):
    return render(request, 'templates/aboutme.html', {'aboutme': aboutme})
# 9. Widok umożliwiający rejestrację.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
