from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name = 'store'), # home page ''
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('login_user/', views.login_user, name='login'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('logout_user/', views.logout_user, name='logout'),

]
