from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.article_list, name='article_list'),
    path('articles/<str:slug>/', views.article_detail, name='article_detail'),
    path('category/<str:slug>/', views.category_detail, name='category_detail'),
    path('tag/<str:slug>/', views.tag_detail, name='tag_detail'),
    path('authors/<str:username>/', views.author_detail, name='author_detail'),
    path('search/', views.search, name='search'),
    path('api/live-search/', views.live_search, name='live_search'),
]

