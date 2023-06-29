from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Post, Category


def index(request):
    '''view-функция index.html'''
    template = 'blog/index.html'
    posts = Post.objects.select_related(
        'location', 'author', 'category').filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )[:5]
    context = {'post_list': posts}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.all(),
        pk=id,
        pub_date__date__lte=timezone.now(),
        category__is_published=True,
        is_published=True)
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    """view-функция category.html"""
    category = get_object_or_404(Category.objects.filter(is_published=True),
                                 slug=category_slug)
    posts = category.posts.select_related(
        'author',
        'location',
        'category',
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,)
    context = {
        'post_list': posts,
        'category': category,
    }
    return render(request, 'blog/category.html', context)
