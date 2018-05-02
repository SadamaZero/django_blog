from django import template
from ..models import Comment
from django.contrib.contenttypes.models import ContentType
from ..forms import CommentForm

register = template.Library()


@register.simple_tag
def comments_count(article):
    content_type = ContentType.objects.get_for_model(article)
    count = Comment.objects.filter(content_type=content_type,
                                   object_id=article.id).count()

    return count


@register.simple_tag
def get_comment_form(article):
    content_type = ContentType.objects.get_for_model(article)

    comment_form_data_init = {}
    comment_form_data_init['content_type'] = content_type
    comment_form_data_init['object_id'] = article.id
    comment_form_data_init['reply_comment_id'] = 0
    form = CommentForm(initial=comment_form_data_init)

    return form


@register.simple_tag
def get_comments_list(article):
    content_type = ContentType.objects.get_for_model(article)
    comments = Comment.objects.filter(content_type=content_type,
                                      object_id=article.id,
                                      parent=None)

    return comments.order_by('-comment_time')
