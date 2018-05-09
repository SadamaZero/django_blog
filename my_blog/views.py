from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.core.paginator import *
from django.db.models import Count
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import *
from django.http import JsonResponse


# Create your views here.
def blog_list(request, index=1):
    blogs = Blog.objects.all()
    pageintor = Paginator(blogs, 10)
    page = pageintor.get_page(index)
    blog_dates_dict = {}
    context = {}
    context['blogs'] = blogs
    context['blog_type'] = BlogType.objects.annotate(blog_count=Count('blog'))  # 增加备注 关联外键模型名小写
    context['page'] = page
    blog_dates = Blog.objects.dates('created_time',
                                    'month',
                                    order='DESC')
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        # .annotate(blog_count=Count('created_time'))
        blog_dates_dict[blog_date] = blog_count
    context['dates'] = blog_dates_dict
    return render(request, 'blog_list.html', context)


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if not request.COOKIES.get('blog_%s_read' % blog_id):
        # blog.read_num += 1  # 阅读量统计
        if ReadNum.objects.filter(blog=blog):
            # 存在博客且关联的阅读量不为空
            readnum = ReadNum.objects.get(blog=blog)
            readnum.read_num += 1
            readnum.save()
        else:
            # 不存在，新建初始值
            readnum = ReadNum()
            readnum.read_num = 1
            readnum.blog = blog
            readnum.save()
    read_num = ReadNum.objects.get(blog=blog).read_num

    # 上下篇跳转链接
    previous_blog = Blog.objects.filter(created_time__gt=blog.created_time).last()
    if previous_blog is None:
        previous_blog = blog

    next_blog = Blog.objects.filter(created_time__lt=blog.created_time).first()
    if next_blog is None:
        next_blog = blog


    context = {}
    context['read_num'] = read_num
    context['blog'] = blog
    context['user'] = request.user
    context['login_form'] = LoginForm()
    # -----------------------自定标签法替代-----------------------------------------

    # 评论表单初始化
    # comment_form_data_init = {}
    # comment_form_data_init['content_type'] = blog_content_type.model
    # comment_form_data_init['object_id'] = blog.id
    # comment_form_data_init['reply_comment_id'] = 0

    # context['comments_count'] = Comment.objects.filter(content_type=blog_content_type,
    #                                                    object_id=blog.id).count()

    # context['comment_form'] = CommentForm(initial=comment_form_data_init)  # 传递初始化参数
    # **************************************************************************
    # comments = Comment.objects.filter(content_type=blog_content_type,
    #                                   object_id=blog.id,
    #                                   parent=None)
    # context['comments'] = comments.order_by('-comment_time')
    # ----------------------------------------------------------------------------
    context['previous_blog'] = previous_blog
    context['next_blog'] = next_blog

    response = render(request, 'blog_detali.html', context)
    response.set_cookie('blog_%s_read' % blog_id, 'true', max_age=60*10)
    return response


def show_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs = Blog.objects.filter(blog_type=blog_type)
    pageintor = Paginator(blogs, 10)
    index = request.GET.get('index', 1)
    page = pageintor.get_page(index)  # get_page()方法，当get得到的参数不是整数，返回第一页
    context = {}
    context['blogs'] = blogs
    context['blog_type'] = blog_type
    context['page'] = page
    return render(request, 'show_type.html', context)


def show_date(request, year, month):
    blogs = Blog.objects.filter(created_time__year=year, created_time__month=month)
    pageintor = Paginator(blogs, 10)
    index = request.GET.get('index', 1)
    page = pageintor.get_page(index)

    context = {}
    context['blogs'] = blogs
    context['page'] = page
    context['year'] = year
    context['month'] = month
    return render(request, 'show_date.html', context)


def login_blog(request):
    # username = request.POST.get('username', '')
    # password = request.POST.get('password', '')
    # user = authenticate(request, username=username, password=password)

    # if user is not None:
    #     login(request, user)
    #     # 重定向
    #     return redirect(referer)
    # else:
    #     # Return an 'invalid login' error message.
    #     return render(request, 'error_login.html',
    #                   {'message': '用户名或密码不正确',
    #                    'redirect_to': referer,
    #                    })
    # referer = request.META.get('HTTP_REFERER', reverse('home'))

    # ---------------django.form 对比 -------------------
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():  # 合法
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                 # 验证成功 重定向
                # if request.is_ajax():
                return redirect(request.GET.get('from', reverse('home')))
            else:
                login_form.add_error(None, '用户名或密码不正确')  # (字段名（无法判断不写具体）， 错误信息)
            # Form类clean方法
            # user = login_form.cleaned_data['user']
            # login(request, user)
            # return redirect(request.GET.get('from', reverse('home')))

    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    # if request.is_ajax():
    return render(request, 'login_page.html', context)


def login_for_medal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():  # 合法
        username = login_form.cleaned_data['username']
        password = login_form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            data['status'] = 'SUCCESS'
        else:
            data['status'] = 'ERROR'
    else:
        data['status'] = 'ERROR'

    return JsonResponse(data)


# 新用户注册
def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            email = register_form.cleaned_data['email']
            user_new = User.objects.create_user(username, email, password)
            user_new.save()
            # 注册成功后自动登陆
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        register_form = RegisterForm()

    context = {}
    context['register_form'] = register_form
    return render(request, 'register.html', context)


# 注销
def logout_view(request):
    logout(request)

    return redirect(request.GET.get('from', reverse('home')))
