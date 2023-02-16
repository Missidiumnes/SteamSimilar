
import pytest
from django.urls import reverse
from .models import Topic, Tag
from django.contrib.auth.models import User
from SteamSimilar.forms import PostForm, CommentForm, LoginForm, SignInForm


@pytest.fixture
def test_topic():
    return Topic.objects.create(title='test topic')


@pytest.fixture
def test_user():
    return User.objects.create_user(
        username='testuser', email='testuser@example.com', password='testpassword')


def test_index(client, test_topic):
    response = client.get(reverse('index'))
    assert response.status_code == 200
    assert test_topic.title.encode() in response.content


def test_topic_view(client, test_topic):
    response = client.get(reverse('topic', args=[test_topic.id]))
    assert response.status_code == 200
    assert test_topic.title.encode() in response.content


@pytest.mark.django_db
def test_new_post(client, test_topic, test_user):
    client.login(username='testuser', password='testpassword')
    response = client.post(reverse('new_post'), {'title': 'test post', 'body': 'blablabla', 'topic_id': test_topic.id})
    assert response.status_code == 302
    assert response.url == reverse('topic', args=[test_topic.id])
    assert test_topic.post_set.first().title == 'test post'
    assert test_topic.post_set.first().body == 'blablabla'
    assert test_topic.post_set.first().author == test_user


@pytest.mark.django_db
def test_new_comment(client, test_topic, test_user):
    client.login(username='testuser', password='testpassword')
    test_post = test_topic.post_set.create(title='test comment', body='blablabla', author=test_user)
    response = client.post(reverse('new_comment'), {'body': 'blablabla', 'post_id': test_post.id})
    assert response.status_code == 302
    assert response.url == reverse('topic', args=[test_topic.id])
    assert test_post.comment_set.first().body == 'blablabla'
    assert test_post.comment_set.first().author == test_user


def test_tags(client):
    response = client.get(reverse('tags'))
    assert response.status_code == 200
    assert Tag.objects.count() == len(response.context['tags'])


@pytest.mark.django_db
def test_login_view(client, test_user):
    response = client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 302
    assert response.url == reverse('index')
    assert client.session['_auth_user_id'] == str(test_user.id)


@pytest.mark.django_db
def test_signin(client, test_user):
    response = client.post(reverse('signin'), {'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 302
    assert response.url == reverse('index')
    assert client.session['_auth_user_id'] == str(test_user.id)


def test_aboutme(client):
    response = client.get(reverse('aboutme'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_register(client):
    response = client.post(reverse('register'), {'username': 'testuser', 'password1': 'testpassword', 'password2': 'testpassword'})
    assert response.status_code == 302
    assert response.url == reverse('index')
    assert User.objects.filter(username='testuser').exists()

@pytest.mark.django_db
def test_post_form_valid():
    form_data = {'text': 'blablabla', 'topic': 'post'}
    form = PostForm(data=form_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_comment_form_valid():
    form_data = {'text': 'blablabla', 'comment': 1}
    form = CommentForm(data=form_data)
    assert form.is_valid()

def test_login_form_valid():
    form_data = {'username': 'jajajaja', 'password': '1234'}
    form = LoginForm(data=form_data)
    assert form.is_valid()

def test_signin_form_valid():
    form_data = {'username': 'ajajajaj', 'password': '123456'}
    form = SignInForm(data=form_data)
    assert form.is_valid()
