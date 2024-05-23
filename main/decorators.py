from functools import wraps
from django.shortcuts import redirect


def user_logged_in(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):

        if 'user_id' in request.session and 'username' in request.session:
            return function(request, *args, **kwargs)
        else:

            return redirect('custom_login')

    return wrapper

def custom_never_cache(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    return _wrapped_view