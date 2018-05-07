def check_user_quota(func):
    """Checks whether a user has enough quota to make an API call"""
    def check_and_call(request, *args, **kwargs):
        user = request.user.siteuser


        if user.groups.filter(name__in=['CEO', 'Manager']).exists():
            return func(request, *args, **kwargs)
        return redirect('/access-denied/')
    return check_and_call