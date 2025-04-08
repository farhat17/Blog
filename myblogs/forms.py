from django import forms
from tinymce.widgets import TinyMCE
from .models import Post,Comment,Profile

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'categories', 'image')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the title here',
                'aria-label': 'Post Title'
            }),
            'content': TinyMCE(attrs={
                'class': 'form-control',
                'rows': 15,
                'placeholder': 'Write your content here',
                'aria-label': 'Post Content'
            }),
            'categories': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check form-check-inline',  
                'aria-label': 'Post Categories'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'aria-label': 'Upload an image',
                'accept': 'image/*'  
            }),
        }


class CommentForm(forms.Form):
   name = forms.CharField(max_length=100)
   email = forms.EmailField()
   content = forms.CharField()
   
   
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your name',
        'aria-label': 'Name'
    }))
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email',
        'aria-label': 'Email'
    }))
    
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Subject of your message',
        'aria-label': 'Subject'
    }))
    
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Write your message here',
        'aria-label': 'Message'
    }))

    