from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import *
from .models import *


class UserAdmin(UserAdmin):
	add_form = RegisterUserForm
	form = UserChangeForm
	model = User
	list_display = ('id', 'username', 'date_joined', 'is_staff')
	list_display_links = ('username',)
#	prepopulated_fields = {'slug': ('username',)}
	 
class Bank_AccountAdmin(admin.ModelAdmin):
	list_display = ('id', 'account', 'time_create')
	list_display_links = ('id', 'account')
	search_fields = ('id', 'account')
	list_filter = ('account', 'time_create')
	
class Account_BalanceAdmin(admin.ModelAdmin):
	list_display = ('id', 'balance')
	list_display_links = ('id', 'balance')

admin.site.register (User, UserAdmin)
admin.site.register (Bank_Account, Bank_AccountAdmin)
admin.site.register (Account_Balance, Account_BalanceAdmin)
