from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.core import validators

'''
class AddClientForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'sex', 'age',]
		widgets = {
			'first_name': forms.TextInput(attrs={'placeholder': 'Введите имя'}),
			'last_name': forms.TextInput(attrs={'placeholder': 'Введите фамилию'}),
			'age': forms.TextInput(attrs={'placeholder': 'Введите возраст'}),
		}
'''
		
class UserChangeForm(UserChangeForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'sex', 'age', 'email']
		
class ProfileChangeForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'sex', 'age', 'email']

class AddBankAccountForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(AddBankAccountForm, self).__init__(*args, **kwargs)
	
	def clean_account(self):
		form_account = self.cleaned_data.get('account')
		existing = Bank_Account.objects.filter(client=self.user, account=form_account).exists()
		if existing:
			raise ValidationError('Такой счёт уже существует')
			
		return form_account
	
	class Meta:
		model = Bank_Account
		fields = ['account']
'''		
class AddBalance(forms.ModelForm):		
	def clean_balance(self):
		form_balance = self.cleaned_data.get('balance')
		if form_balance >= 1000:
			raise ValidationError('Введите меньше 1000')
			
		return form_balance
		
	class Meta:
		model = Account_Balance
		fields = ['balance']
'''
class RegisterUserForm(UserCreationForm):
	username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={}))
	password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={}))
	password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={}))
	
	class Meta:
		model = User
		fields = ['username', 'password1', 'password2',]
		
class ClientsFilterForm(forms.Form):
	sort_selection = (
		('username', 'по алфавиту'),
		('age', 'по возрасту'),
		('sex', 'по полу'),
	)
	ordering = forms.ChoiceField(label='Сортировка', required=False, choices=sort_selection)
	
class AddBalanceForm(forms.Form):
	def __init__(self, *args, **kwargs):
		self.balance = kwargs.pop('balance', None)
		super(AddBalanceForm, self).__init__(*args, **kwargs)
	
	replenishment_amount = forms.IntegerField(label='Сумма пополнения', validators=[validators.MinValueValidator(0),])
	
	def clean_replenishment_amount(self):
		form_replenishment_amount = self.cleaned_data.get('replenishment_amount')
		if form_replenishment_amount >= 1000:
			raise ValidationError('Введите меньше 1000')
		if self.balance+form_replenishment_amount >= 1000 or self.balance > 1000:
			raise ValidationError('Ограничение счёта. Вы больше не можете его пополнять')
			
		return form_replenishment_amount
		
class TransfersForm(forms.Form):
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(TransfersForm, self).__init__(*args, **kwargs)
		self.fields['account_1'].queryset = Bank_Account.objects.filter(client=self.user)
		self.fields['account_2'].queryset = Bank_Account.objects.filter(client=self.user)
	
	account_1 = forms.ModelChoiceField(queryset=None, label='С какого счёта')
	account_2 = forms.ModelChoiceField(queryset=None, label='На какой счёт')
	amount = forms.IntegerField(label='Сумма перевода', validators=[validators.MinValueValidator(0),])
	
	def clean(self):
		if self.cleaned_data['account_1'] == self.cleaned_data['account_2']:
			raise ValidationError('Перевод невозможен. Выбраны одинаковые счета')
# Не получилось сделать валидацию чтобы значения счёта не уходило в минус	
#	def clean_account_1(self):
#		form_amount = self.cleaned_data.get('amount') # по какой то причине это поле возвращает NoneType
#		form_account_1 = self.cleaned_data.get('account_1')
#		account_db = Bank_Account.objects.filter(client=self.user, account=form_account_1)
#		if account_db[0].account_balance.balance-form_amount < 0:
#			raise ValidationError('Недостаточно средств на счёте')
			
#		return form_account_1
				
	def clean_amount(self):
		form_amount = self.cleaned_data.get('amount')
		if form_amount > 1000:
			raise ValidationError('Сумма перевода должна быть меньше 1000')
			
		return form_amount

