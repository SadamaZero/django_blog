from django.urls import path
from . import views

# /user_center/
urlpatterns = [
    path('', views.user_info, name='user_info'),
]
