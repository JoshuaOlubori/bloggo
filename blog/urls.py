from django.urls import path
from . import views
from .views import HomeView, PostListView

app_name = 'blog'

urlpatterns = [
    # post views
    path('', HomeView.as_view(), name='home'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('authors/', views.display_authors, name='display_authors'),
    path('category/', views.category_list, name='category_list'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail, name='post_detail'),
    path('category/<str:category>/', views.get_posts_of_category,
         name='get_posts_of_category'),
    

]

