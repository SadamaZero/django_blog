from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class BlogType(models.Model):
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return self.type_name


class Blog(models.Model):
    title = models.CharField(max_length=50)
    content = RichTextUploadingField()
    # read_num = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)

    def __str__(self):
        return "<Blog:%s>" % self.title

    class Meta:
        ordering = ['-created_time']


class ReadNum(models.Model):
    read_num = models.IntegerField()
    blog = models.OneToOneField(Blog, on_delete=models.CASCADE)  # 一对一字段

    def __str__(self):
        return str(self.read_num)
