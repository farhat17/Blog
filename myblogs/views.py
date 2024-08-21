from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Post, Category
from .forms import PostForm
from .models import Post
from django.contrib.auth import logout as django_logout 


def index(request):
    posts = Post.objects.all().order_by('-created_at')[:4]
    trending_posts = Post.objects.order_by('-created_at')[:3]
    
    context = {
        'posts': posts,
        'trending_posts': trending_posts,
    }
    
    return render(request, 'index.html',context)



def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(username = username).exists():
                messages.error(request,'Username already exists')
            elif User.objects.filter(email = email).exists():
                messages.error(request,'Email already exits')
            else:
                user = User.objects.create_user(username = username,email = email,password = password1)
                user.save()
                messages.success(request,'Account Created Successfully')
                return redirect('index')
        else:
            messages.error(request, 'Passwords do not match')
    return render(request,'signup.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username = username,password = password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.error(request,"Invalid Credentials")
    return render(request,'login.html')        
            

def user_logout(request):
    django_logout(request)
    return redirect('login_user')



@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Check if the current user is the author of the post
    if request.user == post.author:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()  # This will save the post and its related objects
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'post_form.html', {'form': form})
    else:
        return HttpResponseForbidden("You don't have permission to edit this post.")

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        if request.method == 'POST':
            post.delete()
            return redirect('index')
        return render(request, 'post_confirm_delete.html', {'post': post})
    else:
        return HttpResponseForbidden("You don't have permission to delete this post.")

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    trending_posts = Post.objects.order_by('-created_at')
    
    
    return render(request, 'post_detail.html', {'post': post,'trending_posts': trending_posts,})