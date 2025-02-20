from django.shortcuts import redirect
from .models import UserSubscription
from django.utils.timezone import now

def subscription_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect unauthenticated users to login
        subscription = UserSubscription.objects.filter(user=request.user, end_date__gte=now()).first()
        if not subscription or not subscription.is_active:
            return redirect('subscribe')  # Redirect users without active subscriptions
        return view_func(request, *args, **kwargs)
    return wrapper
