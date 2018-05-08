from django.contrib import admin
from .models import *


@admin.register(LikeRecord)
class LikeRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'object_id')


@admin.register(LikeCount)
class LikeCountAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'num_liked', 'content_object')
