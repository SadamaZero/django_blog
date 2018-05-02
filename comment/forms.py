from django import forms
from django.contrib.contenttypes.models import ContentType
from ckeditor.widgets import CKEditorWidget
from .models import Comment


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    comment_text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'))
                                # 在setting中配置ckeditor

    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'reply_comment_id'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 用户是否登陆
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('尚未登陆')

        # 评论对象认证
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']

        try:
            model_class = ContentType.objects.get(model=content_type).model_class()
            model_obj = model_class.objects.get(pk=object_id)
            self.cleaned_data['content_object'] = model_obj
        except Exception as e:
            raise forms.ValidationError('评论失败，请重新提交')

        return self.cleaned_data


    # 回复评论有效性检测
    def clean_reply_comment_id(self):
        reply_comment_id = self.cleaned_data['reply_comment_id']
        if reply_comment_id < 0:
            raise forms.ValidationError('错误')
        elif reply_comment_id == 0:
            self.cleaned_data['parent'] = None
        elif Comment.objects.filter(id=reply_comment_id).exists():
            self.cleaned_data['parent'] = Comment.objects.get(id=reply_comment_id)
        else:
            raise forms.ValidationError('错误')

        return reply_comment_id
