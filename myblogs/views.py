from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
# from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Post, Category,Comment
from .forms import PostForm,CommentForm
from .models import Post,PostReaction,Profile
from django.contrib.auth import logout as django_logout 
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
import re
def is_superuser(user):
    return user.is_superuser

def index(request):
    single_post = Post.objects.all().order_by('-created_at')[:1]
    posts = Post.objects.all().order_by('-created_at')[:4]
    trending_posts = Post.objects.all().order_by('-views')[:2]
    spost = Post.objects.all().order_by('-views')[:1]
    categories = Category.objects.all()
    context = {
        'posts': posts,
        'trending_posts': trending_posts,
        'categories': categories,
        'category':category,
        'single_post':single_post,
        'spost':spost,
        
    }
    
    return render(request, 'index.html',context)



def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if not username:
                messages.error('Username is empty')
            elif User.objects.filter(username = username).exists():
                messages.error(request,'Username already exists')
            elif User.objects.filter(email = email).exists():
                messages.error(request,'Email already exits')
            else:
                user = User.objects.create_user(username = username,email = email,password = password1)
                user.save()
                
                profile = request.FILES.get('profile')  
                bio = request.POST.get('bio', '') 
                Profile.objects.create(
                    user=user,
                    profile=profile,
                    bio=bio
                )
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



# Crete Post                         

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})


#=================== Edit Post ===================================

@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    # Check if the current user is the author of the post
    if request.user == post.author:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()  
                return redirect('post_detail', slug=post.slug)
        else:
            form = PostForm(instance=post)
        return render(request, 'post_form.html', {'form': form})
    else:
        return HttpResponseForbidden("You don't have permission to edit this post.")
    
    
    
    
# Delete Post 
 
@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user == post.author:
        if request.method == 'POST':
            post.delete()
            return redirect('index')
        return render(request, 'post_confirm_delete.html', {'post': post})
    else:
        return HttpResponseForbidden("You don't have permission to delete this post.")
       
# ================= Post Detail =====================================

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    trending_posts = Post.objects.all().order_by('-created_at')[:2]
    categories = Category.objects.all()
    like_count = post.reactions.filter(reaction='like').count()
    dislike_count = post.reactions.filter(reaction='dislike').count()
    user_reaction = post.reactions.filter(user=request.user).first() if request.user.is_authenticated else None
    author = Profile.objects.all()
    context = {
        'post': post,
        'like_count': like_count,
        'dislike_count': dislike_count,
        'user_reaction': user_reaction,
        'trending_posts': trending_posts,
        'categories':categories,
        'author':author,
        'meta_title': post.title,
        'meta_description': post.content[:160],
        'meta_keywords': ', '.join([category.name for category in post.categories.all()]),
    
    }
    
    return render(request, 'post_detail.html', context)
   
# ================= Category_Detail ===================================

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    allcategory = Category.objects.all()
    trending_posts = Post.objects.order_by('-created_at')[:1]
    posts = Post.objects.filter(categories=category)
    # If there are no posts in the category, avoid querying for recommended posts
    if posts.exists():
        # Get the IDs of the categories for the current posts
        category_ids = posts.values_list('categories', flat=True)
        # print(category_ids)

        # Get recommended posts based on those categories
        recommended_posts = Post.objects.filter(categories__in=category_ids).exclude(id__in=posts.values_list('id', flat=True)).distinct()[:5]
        # print(recommended_posts)
    else:
        recommended_posts = Post.objects.none()
        
    context = {
        'category': category, 
        'posts': posts,
        'trending_posts':trending_posts,
        'allcategory':allcategory,
        'recommended_posts': recommended_posts,
        
    }
    return render(request, 'category_detail.html',context)


# ========================= category ======================

def category(request):
    categories = Category.objects.all() 
    trending_posts = Post.objects.all().order_by('created_at')[:1]
    
    return render(request, 'category_list.html', {'categories': categories,'trending_posts':trending_posts})

# Comment 


def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    print(post)
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        print(name)
        email = request.POST.get('email').strip()
        content = request.POST.get('content').strip()
        errors = {}

        # Basic Validation
        if not name:
            errors['name'] = 'Name is required.'
        if not email or not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            errors['email'] = 'Invalid email address.'
        if not content:
            errors['content'] = 'Content is required.'
        elif len(content) > 500:
            errors['content'] = 'Content should not exceed 500 characters.'

        # If errors, show them in the form
        if errors:
            return render(request, 'post_detail.html', {
                'post': post, 
                'form': {'name': name, 'email': email, 'content': content}, 
                'errors': errors
            })

        # Save the comment
        comment = Comment(name=name, email=email, content=content, post=post)
        comment.save()

        # Optionally use messages to show success
        messages.success(request, 'Your comment has been posted successfully!')
        
        # Redirect back to the post detail page
        return redirect('post_detail', slug=slug)

    # If GET request, just render the form
    return render(request, 'post_detail.html', {'post': post})


# Like/Dislike 

def react_to_post(request, slug, reaction_type):
    # Get the post
    post = get_object_or_404(Post, slug=slug)
    
    # Define valid reactions
    valid_reactions = dict(PostReaction.REACTION_CHOICES).keys()
    if reaction_type not in valid_reactions:
        return redirect('post_detail', slug=post.slug)
    
    # Check for user session or authenticated user
    session_key = request.session.session_key or request.session.create()
    user = request.user if request.user.is_authenticated else None

    # Check if the user has already reacted to the post
    existing_reaction = PostReaction.objects.filter(post=post, user=user, session_key=session_key).first()

    if existing_reaction:
        if existing_reaction.reaction == reaction_type:
            # Remove reaction if the same reaction is clicked again
            existing_reaction.delete()
            current_reaction = None
        else:
            # Update to the new reaction
            existing_reaction.reaction = reaction_type
            existing_reaction.save()
            current_reaction = reaction_type
    else:
        # Create a new reaction
        PostReaction.objects.create(post=post, user=user, session_key=session_key, reaction=reaction_type)
        current_reaction = reaction_type

    # Get updated reaction counts
    reaction_counts = {
        reaction: post.reactions.filter(reaction=reaction).count()
        for reaction in valid_reactions
    }

    # Return updated counts as JSON
    response_data = {
        'like_count': reaction_counts.get('like', 0),
        'dislike_count': reaction_counts.get('dislike', 0),
        'love_count': reaction_counts.get('love', 0),
        'current_reaction': current_reaction,
    }

    return JsonResponse(response_data)

@login_required
@user_passes_test(is_superuser)
def approve_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_superuser:  
        post.approved = True
        post.save()
        return redirect('post_list')
    else:
        return redirect('no_permission')  

@login_required
@user_passes_test(is_superuser)
def disapprove_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_superuser:  
        post.approved = False
        post.save()
        return redirect('post_list')
    else:
        return redirect('no_permission')  
    
    
    
def post_list(request):
        posts = Post.objects.filter(approved=True)  
        trending_posts = Post.objects.order_by('-views')[:1]
        sposts = Post.objects.all().order_by('-views')[:2]
        categories = Category.objects.all()
        
        context = {
            'posts': posts,
            'trending_posts':trending_posts,
            'sposts':sposts,
            'categories':categories
            }
        return render(request, 'post_list.html',context )
    
    
#  ===================== Seach ======================================

def search(request):
    query = request.GET.get('search', '')
    if query:
        posts = Post.objects.filter(title__icontains=query) | Post.objects.filter(content__icontains=query)
    else:
        posts = Post.objects.none()  

    return render(request, 'index.html', {'query': query, 'posts': posts})
    
def no_permission(request):
    return render(request, 'no_permission.html')



def author_detail(request, username):
    # Fetch the user and their profile
    author = get_object_or_404(User, username=username)
    
    # Fetch all posts by the author
    author_posts = Post.objects.filter(author=author)
    
    return render(request, 'about.html', {
        'post': author_posts.first(),  # Pass the first post for the profile section
        'author_posts': author_posts,  # All posts by this author
    })