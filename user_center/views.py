from django.shortcuts import render
from . import my_decorator
from .forms import BlogForm
from my_blog import models


@my_decorator.login_status
def user_info(request):
    context = {}
    return render(request, 'user_center/user_info.html', context)


@my_decorator.login_status
def user_write_article(request):
    context = {
        'blog_form': BlogForm()
    }
    return render(request, 'user_center/write_article.html', context)


@my_decorator.login_status
def article_commit(request):
    blog_form = BlogForm(request.POST)

    new_blog = models.Blog()
    new_blog.title = blog_form.data['title']
    new_blog.content = blog_form.data['context']
    new_blog.author = request.user
    new_blog.blog_type = models.BlogType.objects.get(id=3)  # user_article
    # new_blog.save()
    return render(request, 'user_center/user_info.html')
