from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name = 'index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.user_logout, name='logout'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
]
