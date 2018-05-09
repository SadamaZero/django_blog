from django.shortcuts import render


# Create your views here.
def user_info(request):
    context = {}
    return render(request, 'user_center/user_info.html', context)
