from django.shortcuts import redirect, render
from functools import wraps

def is_group(group_names):
    def check_staff_status(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            """
            Confirms if authenticated user belongs to group_names
            """
            allowed = True
            groups = request.user.groups.all()
            if not request.user.is_superuser:
                for group in groups:
                    if group.name not in group_names:
                        allowed = False
                        break 
                if not allowed or not groups.count():
                    return redirect('index')
            return view_func(request, *args, **kwargs)
        return wrapper
    return check_staff_status

def is_verified(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_verified:
            return render(request, 'pages/not-verified.html')
        return view_func(request, *args, **kwargs)
    return wrapper
