from django.urls import path
from .views import *

urlpatterns = [
    path ('', main, name='main'), # 127.0.0.2:8000/
    path ('list_clients/', list_clients, name='list_clients'), # 127.0.0.2:8000/list_clients/
    path ('transactions/', transactions, name='transactions'), # 127.0.0.2:8000/transactions/
    path ('login/', LoginUser.as_view(), name='login'), # 127.0.0.2:8000/login/
    path ('logout/', logout_user, name='logout'),
    path ('register/', RegisterUser.as_view(), name='register'), # 127.0.0.2:8000/register/
    path ('change_profile/', ChangeProfile.as_view(), name='change_profile'),
    path ('client_info/<slug:client_slug>',  client_info, name='client_info'), 
#    path ('add_client/', add_client, name='add_client'), # 127.0.0.2:8000/add_client/
    path ('add_account/', add_account, name='add_account'),
    path ('add_balance/<int:account_balance_pk>', add_balance, name='add_balance'),
    path ('del_account/<int:account_pk>', del_account, name='del_account'),
    path ('transfers/', transfers, name='transfers'),
]
