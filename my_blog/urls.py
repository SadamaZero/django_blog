from django.urls import path
from . import views


# /blog/
urlpatterns = [
    # /blog/<int:id>
    path('<int:blog_id>', views.blog_detail, name='blog_detail'),
    path('type_<int:blog_type_pk>/', views.show_type, name='show_type'),
    path('date/<int:year>/<int:month>/', views.show_date, name='show_date'),
    path('login/', views.login_blog, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
]