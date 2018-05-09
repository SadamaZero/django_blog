"""django_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from my_blog.views import blog_list, login_blog, register, logout_view, login_for_medal


urlpatterns = [
    path('', blog_list, name='home'),
    path('<int:index>/', blog_list),
    path('admin/', admin.site.urls),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('blog/', include('my_blog.urls')),
    path('comment/', include('comment.urls')),
    path('like_it/', include('like_it.urls')),
    path('login/', login_blog, name='login'),
    path('login_medal/', login_for_medal, name='login_for_medal'),  # ajax弹出框登陆
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('user_center/', include('user_center.urls')),
    path('search/', include('haystack.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
