from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.forms import ValidationError
from .models import Driver, Manager


class DriverInline(admin.StackedInline):
    model = Driver
    can_delete = False

class ManagerInline(admin.StackedInline):
    model = Manager
    can_delete = False

class CustomUserAdmin(UserAdmin):
	inlines = (DriverInline, ManagerInline)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
	list_display = ['user', 'full_name']
	search_fields = ['user__username', 'full_name']

	def save_model(self, request, obj, form, change):
		obj.save()

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
	list_display = ['user', 'full_name']
	search_fields = ['user__username', 'full_name']

	def save_model(self, request, obj, form, change):
		obj.save()