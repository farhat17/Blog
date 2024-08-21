from django import forms
from tinymce.widgets import TinyMCE
from .models import Post,Comment,Profile

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'categories', 'image')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': TinyMCE(attrs={'class': 'form-control', 'rows': 15}),  # Adjust rows as needed
            'categories': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields = ['author_name', 'author_email', 'content']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']