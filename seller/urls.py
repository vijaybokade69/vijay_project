from django.urls import path
from .views import *

urlpatterns =[
    path('',seller_index,name = 'seller_index'),
    path('profile/',profile,name = 'profile'),
    path('seller_register/',seller_register,name  = 'seller_register'),
    path('seller_otp/',seller_otp,name  = 'seller_otp'),
    path('seller_login/',seller_login,name  = 'seller_login'),
    path('seller_logout/',seller_logout,name  = 'seller_logout'),
    path('seller_forget/',seller_forget,name  = 'seller_forget'),
    path('seller_edit/',seller_edit,name  = 'seller_edit'),
    path('add_product/',add_product,name = 'add_product'),
    path('my_products/',my_products,name = 'my_products'),
    path('edit_product/<int:pk>',edit_product,name = 'edit_product'),
    path('del_product/<int:pk>',del_product,name = 'del_product'),
    path('change_status/<int:pk>',change_status,name = 'change_status'),



    
    
    
]