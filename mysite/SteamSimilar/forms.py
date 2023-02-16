from django import forms
from .models import Post, Comment
from django.contrib.auth.forms import AuthenticationForm

# 1. Wykorzystywany do tworzenia postów.
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'topic']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your post'}),
            'topic': forms.Select(attrs={'class': 'form-control'}),
        }

# 2. Wykorzystywany do tworzenia komentarzy.
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'post']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your comment'}),
            'post': forms.HiddenInput(),
        }

# 3. Wykorzystywany do logowania.
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}))

# 4. Wykorzystywany do rejestracji.
class SignInForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
