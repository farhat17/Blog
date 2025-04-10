from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.user_logout, name='logout'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/edit/', views.edit_post, name='edit_post'),
    path('post/<slug:slug>/delete/', views.delete_post, name='delete_post'),
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),  # Keep this line
    path('post/<slug:slug>/react/<str:reaction_type>/', views.react_to_post, name='react_to_post'),
    path('categories/', views.category, name='category_list'),
    path('postlist/', views.post_list, name='post_list'),
    path('approve_post/<slug:slug>/', views.approve_post, name='approve_post'),
    path('disapprove_post/<slug:slug>/', views.disapprove_post, name='disapprove_post'),
    path('search/', views.search, name='search'),
    path('author/<str:username>/', views.author_detail, name='author_detail'),
    path('no_permission/', views.no_permission, name='no_permission'),
    path('lifestyle/', views.lifestyle_home, name='lifestyle_home'),
    path('<slug:category_slug>/', views.category_page, name='category_page'),
    path('contact/', views.contact_us,name="contact_us"),
    # path('wellness/', views.wellness, name='wellness'),
    # path('travel/', views.travel, name='travel'),
    # path('fashion/', views.fashion, name='fashion'),
    # path('home-living/', views.home_living, name='home_living'),
    # path('subscribe/', views.subscribe, name='subscribe'),
    # path('section/<slug:slug>/', views.section_detail, name='section_detail'),
]
