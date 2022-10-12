from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.

def post_list(request):
    posts = Post.published.all()
    #likes = Post
    post_list = []
    for post in posts:
        
        post_list.append({'post':post})
    context = {'posts': post_list}
    return render(request, 'blog/home.html', context)

def post_detail(request, id):
    post = get_object_or_404(Post,id=id,status=Post.Status.PUBLISHED)
    return render(request, 'blog/view_post.html')

def category_list(request):
    return render(request, 'blog/category.html')