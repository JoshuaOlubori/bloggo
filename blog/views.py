from django.shortcuts import render, get_object_or_404
from .models import Post, Comment, Like
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView
from .forms import CommentForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json

# Create your views here.
class HomeView(ListView):
    queryset=Post.published.all()[:5]
    context_object_name='posts'
    template_name='blog/home.html'

    def get_context_data(self, **kwargs):
        
        et = super(HomeView, self).get_context_data(**kwargs)
        et['comments'] = Comment.objects.filter(active=True).count()
        et['likes'] = Like.objects.count()
        return et
        

class PostListView(ListView):
    queryset=Post.published.all()
    context_object_name='all_posts'
    template_name='blog/post_list.html'
    paginate_by=4

#def home(request):
#    posts = Post.published.all()[:5]
#    return render(request, 'blog/home.html', {'posts':posts})
#
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,status=Post.Status.PUBLISHED,
    slug=post,
publish__year=year,
publish__month=month,
publish__day=day)
    likes = Like.objects.filter(post=post).count()
    comments =Comment.objects.filter(post=post).filter(active=True)

    return render(request, 'blog/view_post.html', {'post': post, 'likes':likes, 'comments': comments})


@login_required
def like(request):
	post_id = request.GET.get("likeId", "")
	user = request.user
	post = Post.objects.get(pk=post_id)
	liked= False
	like = Like.objects.filter(user=user, post=post)
	if like:
		like.delete()
	else:
		liked = True
		Like.objects.create(user=user, post=post)
	resp = {
        'liked':liked
    }
	response = json.dumps(resp)
	return HttpResponse(response, content_type = "application/json")


def category_list(request):
    return render(request, 'blog/all_category.html')



#class GetPostsofCategory(ListView):               potential class-based alternative to the below
#    queryset=Post.objects.filter(category=category)
#    context_object_name='posts'
#    template_name='blog/category.html'
#    paginate_by=2

def get_posts_of_category(request, category):
    post_list = Post.objects.filter(category=category)
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer, deliver the first page
        posts=paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/category.html', {'posts': posts})

#def get_all_authors(request):
#    authors = Post.objects_set.all()
#    number_of_authors = len(authors)
#    return render(request, 'blog/home.html', {'number_of_authors': number_of_authors})

#class list_authors(ListView):
#    queryset=Post.objects.author_set.all()
#    context_object_name='all_posts'
#    template_name='blog/post_list.html'

#def list_authors(request):
#    contributor = Post.o
#

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment=None
    # A comment was posted 
    form=CommentForm(data=request.POST)
    if form.is_valid():
        # create a comment object without saving it to the database
        comment=form.save(commit=False)
        # assign the post to the comment
        comment.post = post
        # save the comment to the database
        comment.save()
    return render(request, 'blog/view_post.html', {'post':post, 'form': form, 'comment':comment })

def display_authors(request):
    posts = Post.objects.all()
    return render(request, 'blog/authors.html', {'posts':posts})

def return_to_home(request):
    return render(request, 'blog/home.html')


    

