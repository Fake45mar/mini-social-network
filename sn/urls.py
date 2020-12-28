from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('create_post', views.create_post, name='create_post'),
    path('like', views.like, name='like'),
    path('dislike', views.dislike, name='dislike')
]
