from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Category(models.TextChoices):
        NATURE = 'NATURE', 'Nature'
        EDUCATION = 'EDUCATION', 'Education'
        PETS_AND_ANIMALS = 'PETS AND ANIMALS', 'Pets and animals'
        TECHNOLOGY = 'TECHNOLOGY', 'Technology'
        FASHION = 'FASHION', 'Fashion'
        ENTERTAINMENT = 'ENTERTAINMENT', 'Entertainment'
        MOVIES = 'MOVIES', 'Movies'
        GAMING = 'GAMING', 'Gaming'
        MUSIC = 'MUSIC', 'Music'
        SPORTS = 'SPORTS', 'Sports'
        NEWS = 'NEWS', 'News'
        TRAVEL = 'TRAVEL', 'Travel'
        COMEDY = 'COMEDY', 'Comedy'
        DESIGN_AND_DEVELOPMENT = 'DESIGN_AND_DEVELOPMENT', 'Design and Development'
        FOOD_AND_DRINKS = 'FOOD_AND_DRINKS', 'Food and Drinks'
        LIFESTYLE = 'LIFESTYLE', 'Lifestyle'
        HEALTH_AND_FITNESS = 'HEALTH_AND_FITNESS', 'Health and Fitness'
        BUSINESS = 'BUSINESS', 'Business'
        SHOPPING = 'SHOPPING', 'Shopping'
        ANIMATIONS = 'ANIMATIONS', 'Animations'

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    category = models.CharField(max_length=50, choices=Category.choices)
    cover = models.ImageField(upload_to='image', default='default.png')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT)

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])

    def all_posts(self):
        return reverse('blog:post_list')


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    commenter = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]

    def __str__(self):
        return f'Comment by {self.commenter} on {self.post}'


class Like(models.Model):
    liker = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['liked_at']

    def __str__(self):
        return f'Liked by {self.liker} on {self.post}'
