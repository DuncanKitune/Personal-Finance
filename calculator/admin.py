from django.contrib import admin
from .models import UserSubscription, SubscriptionPlan
from django.utils.translation import gettext_lazy as _

# Register your models here.

class IsActiveFilter(admin.SimpleListFilter):
    title = _('Subscription Status')  # A user-friendly title
    parameter_name = 'is_active'  # The URL query parameter

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the dropdown. The second element is the
        human-readable name for the option that will appear
        in the dropdown.
        """
        return (
            ('active', _('Active')),
            ('inactive', _('Inactive')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == 'active':
            return queryset.filter(start_date__lte=timezone.now().date(),
                                    end_date__gte=timezone.now().date())
        if self.value() == 'inactive':
            return queryset.exclude(start_date__lte=timezone.now().date(),
                                     end_date__gte=timezone.now().date())

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date')
    search_fields = ('user__username', 'plan__name')
    list_filter = ('plan__name', 'end_date')

    def is_active(self, obj): #Show result in admin list display
            return obj.is_active

    is_active.boolean = True #Show True / False icon
    is_active.short_description = 'Is Active?'
        
@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days', 'subscribers')
    search_fields = ('name',)
    list_filter = ('duration_days',)





