from django.shortcuts import render, get_object_or_404
from .models import Post
from .utils import total_author_counts

# Create your views here.

def post_list(request):
    posts = Post.published.all()
    #likes = Post
    post_list = []
    for post in posts:
        
        post_list.append({'post':post})
    context = {'posts': post_list}
    return render(request, 'blog/home.html', context)

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,status=Post.Status.PUBLISHED,
    slug=post,
publish__year=year,
publish__month=month,
publish__day=day)

    return render(request, 'blog/view_post.html')

def category_list(request):
    return render(request, 'blog/all_category.html')

def get_posts_of_category(request, category):
    posts = Post.objects.filter(category=category)
    return render(request, 'blog/category.html', {'posts': posts})

#def get_all_authors(request):
#    authors = Post.objects_set.all()
#    number_of_authors = len(authors)
#    return render(request, 'blog/home.html', {'number_of_authors': number_of_authors})

def display_authors(request):
    return render(request, 'blog/authors.html')

def return_to_home(request):
    return render(request, 'blog/home.html')

def total_authors(request):
    authors = Post.objects.author.all()