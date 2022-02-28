from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from slugify import slugify
from django.contrib.auth.decorators import login_required 
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import F


menu = [{'title': 'Главная страница', 'url_name': 'main'},
		{'title': 'Список клиентов', 'url_name': 'list_clients'},
		{'title': 'Последние транзакции', 'url_name': 'transactions'},
]

def main (request):
    return render (request, 'bank/main.html', {'menu': menu, 'title': 'Главная страница'})

def list_clients (request):
	clients = User.objects.all()
	form = ClientsFilterForm(request.GET)
	if form.is_valid():
		if form.cleaned_data.get('ordering'):
			clients = clients.order_by(form.cleaned_data.get('ordering'))
	
	return render (request, 'bank/list_clients.html', {'menu': menu, 'clients': clients, 'form': form, 'title': 'Список клиентов'})

def transactions (request):
    return render (request, 'bank/transactions.html', {'menu': menu, 'title': 'Последние транзакции'})
    
class RegisterUser(CreateView):
	form_class = RegisterUserForm
	template_name = 'bank/register.html'
	success_url = reverse_lazy('main')
	
	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['menu'] = menu
		context['title'] = 'Регистрация'
		return context
		
	def form_valid(self, form):
		user = form.save(commit=False)
		user.slug = slugify(user.username)
		user.save()
		login(self.request, user)
		return redirect('main')
		
class LoginUser(LoginView):
	form_class = AuthenticationForm
	template_name = 'bank/login.html'
	
	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['menu'] = menu
		context['title'] = 'Авторизация'
		return context
		
	def get_success_url(self):
		return reverse_lazy('main')
		
def logout_user(request):
	logout(request)
	return redirect ('login')
	
class ChangeProfile(TemplateView):
	form_class = ProfileChangeForm
	template_name = 'bank/change_profile.html'
		
	def dispatch(self, request, *args, **kwargs):
		form = ProfileChangeForm(instance=request.user)
		if request.method == 'POST':
			form = ProfileChangeForm(request.POST, instance=request.user)
			slug_user = request.user
			if form.is_valid():
				form.save()
				return redirect(reverse_lazy('client_info', args=[slug_user.slug]))
		
		return render (request, 'bank/change_profile.html', {'form': form, 'title': 'Редактировать профиль', 'menu': menu})
		
   
def client_info (request, client_slug):
    client = get_object_or_404 (User, slug=client_slug)
    context={'menu': menu,
			 'client': client,
			 'title': 'Информация о клиенте',
    }
    
    return render (request, 'bank/client_info.html', context=context)
'''
def add_client (request):
	if request.method == 'POST':
		form = AddClientForm(request.POST)
		if form.is_valid():
			addclient = form.save(commit=False)
			addclient.slug = slugify(addclient.first_name+' '+addclient.last_name)
			addclient.save()
			messages.success(request, 'Вы успешно зарегистрировались!')
			return redirect('list_clients')
		else:
			messages.error(request, 'Ошибка регистрации')
	else:
		form = AddClientForm()
		
	return render (request, 'bank/add_client.html', {'menu': menu, 'form': form, 'title': 'Создание клиента'})
'''	
def add_account (request):
	user = request.user
	if request.method == 'POST':
		form = AddBankAccountForm(request.POST, user = request.user)
		if form.is_valid():
			add_account = form.save(commit=False)
			add_account.client = user
			add_account.save()
			return redirect(reverse_lazy('client_info', args=[user.slug]))
	else:
		form = AddBankAccountForm()
	
	return render (request, 'bank/add_account.html', {'menu': menu, 'form': form, 'title': 'Создание счёта'})
	
def add_balance (request, account_balance_pk):
	account_balance = get_object_or_404 (Account_Balance, pk=account_balance_pk)
	
	if request.method == 'POST':
		form = AddBalanceForm(request.POST, balance=account_balance.balance)
		if form.is_valid():
			add_amount = form.cleaned_data.get('replenishment_amount')
			account_balance.balance = F('balance')+add_amount
			account_balance.save()
			return redirect(reverse_lazy('client_info', args=[request.user.slug]))
	else:
		form = AddBalanceForm()
	
	return render (request, 'bank/add_balance.html', {'menu': menu, 'form': form, 'account_balance': account_balance, 'title': 'Пополнение баланса'})

def del_account (request, account_pk):
	account = get_object_or_404 (Bank_Account, pk=account_pk)
	account.delete()
	return redirect(reverse_lazy('client_info', args=[request.user.slug]))
	
def transfers (request):
	if request.method == 'POST':
		form = TransfersForm(request.POST, user = request.user)
		if form.is_valid():
			field_amount = form.cleaned_data.get('amount')
			writeoffs = form.cleaned_data.get('account_1')
			writeoffs.account_balance.balance = F('balance')-field_amount
			replenishment = form.cleaned_data.get('account_2')
			replenishment.account_balance.balance = F('balance')+field_amount
			writeoffs.save()
			replenishment.save()
			return redirect(reverse_lazy('client_info', args=[request.user.slug]))
	else:
		form = TransfersForm(user = request.user)
		
	return render (request, 'bank/transfers.html', {'menu': menu, 'form': form, 'title': 'Переводы между счетами'})
