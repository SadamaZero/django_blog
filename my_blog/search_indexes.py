# coding=utf-8
from haystack import indexes
from .models import Blog


class BlogIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Blog

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
