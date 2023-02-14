from django.urls import path
from .views import *

urlpatterns = [
path('about/',about,name = 'about'),
path('checkout/',checkout,name = 'checkout'),
path('contact/',contact,name = 'contact'),
path('faqs/',faqs,name = 'faqs'),
path('help/',help,name = 'help'),
path('',index,name = 'index'),
path('payment/',payment,name = 'payment'),
path('privacy/',privacy,name = 'privacy'),
path('product/',product,name = 'product'),
path('product2/',product2,name = 'product2'),
path('single/',single,name = 'single'),
path('single2/',single2,name = 'single2'),
path('terms/',terms,name = 'terms'),
path('add_row/',add_row, name = 'add_row'),
path('del_row/',del_row, name = 'del_row'),
path('register/',register,name = 'register'),
path('otp/',otp,name = 'otp'),
path('login/',login,name = 'login'),
path('logout/',logout,name = 'logout'),
path('forget/',forget,name = 'forget'),
path('edit_profile/',edit_profile,name = 'edit_profile'),
path('reset/',reset,name = 'reset'),
path('add_to_cart/<int:pk>',add_to_cart,name = 'add_to_cart'),
path('del_cart_row/<int:pk>',del_cart_row,name = 'del_cart_row'),
path('checkout/paymenthandler/', paymenthandler, name='paymenthandler'),








]