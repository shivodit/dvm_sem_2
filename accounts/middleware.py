from django.shortcuts import redirect
from django.urls import resolve

def check_userprofile_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        ex_url = ['profile_menu','seller_profile_complete','customer_profile_complete','logout']

        if not request.user.is_authenticated:
            return get_response(request)
        
        if not request.user.is_customer and not request.user.is_seller and (resolve(request.path).url_name not in ex_url):
            return redirect("profile_menu")

        response = get_response(request)

        return response

    return middleware