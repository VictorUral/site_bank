from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core import validators


class User(AbstractUser): # Первичная модель
	sex_choices = (
		(' ', 'Не выбран'),
		('М', 'Мужской'),
		('Ж', 'Женский'),
	)
	first_name = models.CharField(max_length=30, blank=True, verbose_name='Имя')
	last_name = models.CharField(max_length=30, blank=True, verbose_name='Фамилия')
	sex = models.CharField(choices=sex_choices, default=' ', max_length=2, verbose_name='Пол')
	age = models.IntegerField(default=0, verbose_name='Возраст')
	slug = models.SlugField(max_length=255, unique=True, db_index=True)

	def __str__(self):
		return self.username
	
	def info(self):
		info = self.first_name + ' ' + self.last_name + ', пол: ' + self.sex + ', возраст: ' + str(self.age)
		return info
		
	def get_absolute_url(self):
		''' Формирует маршрут к конкретной записи из БД '''
		return reverse('client_info', kwargs={'client_slug': self.slug})
		
	def save(self, *args, **kwargs):
		#value = self.username
		self.slug = slugify(self.username, allow_unicode=True)
		super().save(*args, **kwargs)
		
	class Meta: # изменят наименование моедли в админ панели
		verbose_name = 'Пользователи'
		verbose_name_plural = 'Пользователи' # наименование для множемтвенного числа
#		ordering = ['time_create'] # сортировка по времени создания


class Bank_Account (models.Model): # Вторичная модель
	account_choices = (
		('USD', 'USD'),
		('EUR', 'EUR'),
		('RUB', 'RUB'),
	)
	account = models.CharField(choices=account_choices, max_length=3, verbose_name='Счёт')
	time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
	client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Клиент')

	def __str__(self):
		return self.account
			
	def del_account_url(self):
		return reverse('del_account', kwargs={'account_pk': self.pk})
		
	class Meta: 
		verbose_name = 'Банковские счета'
		verbose_name_plural = 'Банковские счета' 
		ordering = ['time_create']
		
class Account_Balance (models.Model):
	bank_account = models.OneToOneField(Bank_Account, on_delete=models.CASCADE)
	balance = models.IntegerField(default=0, validators=[validators.MinValueValidator(0),], verbose_name='Баланс')
	
	def __str__(self):
		return self.balance
		
	def get_absolute_url(self):
		return reverse('add_balance', kwargs={'account_balance_pk': self.pk})
	
	class Meta:
		verbose_name = 'Баланс счёта'
		
	@receiver(post_save, sender=Bank_Account)
	def create_user_bank_account(sender, instance, created, **kwargs):
		if created:
			Account_Balance.objects.create(bank_account=instance)
			
	@receiver(post_save, sender=Bank_Account)
	def save_user_bank_account(sender, instance, **kwargs):
		instance.account_balance.save()
