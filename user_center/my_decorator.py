from django.http import HttpResponseRedirect


def login_status(func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' in request.session:
            return func(request, *args, **kwargs)
        else:
            redirect = HttpResponseRedirect('/blog/login/?from=/user_center/')
            return redirect
    return wrapper
