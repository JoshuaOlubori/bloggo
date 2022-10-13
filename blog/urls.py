from django.urls import path
from . import views
from .views import PostListView, home

app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.home, name='home'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('authors/', views.display_authors, name='display_authors'),
    path('category/', views.category_list, name='category_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail, name='post_detail'),
    path('category/<str:category>/', views.get_posts_of_category,
         name='get_posts_of_category'),
    

]

