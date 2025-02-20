from django.shortcuts import redirect
from django.utils.timezone import now
from django.urls import reverse
from .models import UserSubscription

class SubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip middleware for non-authenticated users or public pages
        if not request.user.is_authenticated:
            return self.get_response(request)

        # Check subscription status
        try:
            subscription = UserSubscription.objects.get(user=request.user)
            if not subscription.is_active:
                return redirect(reverse('subscribe'))  # Redirect to subscription page
        except UserSubscription.DoesNotExist:
            return redirect(reverse('subscribe'))  # Redirect if no subscription exists

        return self.get_response(request)
