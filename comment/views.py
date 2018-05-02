from django.shortcuts import render, redirect, reverse
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from .forms import CommentForm
from django.http import JsonResponse


# Create your views here.
def update_comment(request):
    # referer = request.META.get('HTTP_REFERER', reverse('home'))
    # content_text = request.POST.get('comment_text', '').strip()  # 多个空格去掉
    #
    # # 内容有效检测
    # if content_text == '':
    #     return render(request, 'error_login.html',
    #                   {'message': '无效评论',
    #                    'redirect_to': referer,
    #                    })
    # try:
    #     content_type = request.POST.get('content_type', '')
    #     object_id = int(request.POST.get('object_id', ''))
    #     model_class = ContentType.objects.get(model=content_type).model_class()
    #     model_obj = model_class.objects.get(pk=object_id)
    # except Exception as e:
    #     return render(request, 'error_login.html',
    #                   {'message': '评论提交失败,请重新提交',
    #                    'redirect_to': referer
    #                    })
    #
    # comment = Comment()
    # comment.user = request.user
    # comment.text = content_text
    # comment.content_object = model_obj
    # comment.save()
    #
    # return redirect(referer)
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}
    if comment_form.is_valid():
        # 保存评论
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['comment_text']
        comment.content_object = comment_form.cleaned_data['content_object']  # ！！

        # 二级回复操作
        parent = comment_form.cleaned_data['parent']
        if parent is not None:
            comment.root = parent.root if parent.root is not None else parent
            comment.parent = parent
            comment.reply_to = parent.user
            data['reply_to'] = comment.reply_to.username
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if comment.root is not None else ''
        comment.save()
        # return redirect(referer)

        # ------Ajax------
        # ----返回数据-----

        data['status'] = 'SUCCESS'
        data['username'] = comment.user.username

        # --------------------!!!!!-----------------------
        # ---------------Ajax .strftime()直接格式化，去掉了时区信息------------
        # 时间错误：data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        # --------------正确处理：timestamp() 时间戳方法(距格林威治时间1970.1.1-00：00：00的秒数)--------------------
        data['comment_time'] = comment.comment_time.timestamp()  # 需要还原格式

        data['comment_text'] = comment.text

        return JsonResponse(data)
    else:
        # return render(request, 'error_login.html',
        #               {'message': comment_form.errors,
        #                'redirect_to': referer
        #               })
        data = {}
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
        return JsonResponse(data)
