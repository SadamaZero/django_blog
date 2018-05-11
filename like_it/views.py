from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from django.http import JsonResponse
from .models import LikeCount, LikeRecord


def like_change(request):
    user = request.user
    if not user.is_authenticated:
        return error_response(400, '请先登录')

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))

    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return error_response(401, 'ObjectDoesNotExist')

    if request.GET.get('like_flag') == 'true':
        # 赞
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type,
                                                                object_id=object_id,
                                                                user=user)
        if created:
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type,
                                                                  object_id=object_id)
            like_count.num_liked += 1
            like_count.save()
            return success_to_response(like_count.num_liked)
        else:
            # 已点赞，不能重复
            return error_response(402, 'error:repeat like commit.')
    else:
        # 取消
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            record.delete()

            like_content, created = LikeCount.objects.get_or_create(content_type=content_type,
                                                                    object_id=object_id)
            if not created:
                like_content.num_liked -= 1
                like_content.save()
                return success_to_response(like_content.num_liked)
            else:
                return error_response(404, 'data error')
        else:  # 错误 不存在
            return error_response(403, 'no data.')


def success_to_response(num_like):
    data = {
        'status': 'success',
        'num_liked': num_like
    }
    return JsonResponse(data)


def error_response(code, message):
    data = {
        'status': 'error',
        'code': code,
        'message': message
    }
    return JsonResponse(data)
