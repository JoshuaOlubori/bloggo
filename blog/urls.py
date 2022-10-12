from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    path('', views.return_to_home, name='return_to_home'),
    path('authors/', views.display_authors, name='display_authors'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail, name='post_detail'),
    path('category/<str:category>/', views.get_posts_of_category,
         name='get_posts_of_category'),
    path('category/', views.category_list, name='category_list'),

]
