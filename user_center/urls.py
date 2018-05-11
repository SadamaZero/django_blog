from django.urls import path
from . import views

# /user_center/
urlpatterns = [
    path('', views.user_info, name='user_info'),
    path('new_article/', views.user_write_article, name='write_article'),
    path('article_commit', views.article_commit, name='article_commit'),
]
