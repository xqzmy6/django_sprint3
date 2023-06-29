from django.shortcuts import render, get_object_or_404

from .models import Post, Category
from django.utils import timezone


def index(request):
    '''view-функция index.html'''
    template = 'blog/index.html'
    post = Post.objects.select_related(
        'location', 'author', 'category').filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )[:5]
    context = {'post_list': post}
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
    post_list = category.post_set.select_related(
        'author',
        'location',
        'category',
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,)
    context = {
        'post_list': post_list,
        'category': category,
    }
    return render(request, 'blog/category.html', context)
