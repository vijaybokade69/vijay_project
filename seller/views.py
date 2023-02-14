from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.conf import settings
import random



# Create your views here.
def seller_index(request):
    try:
        seller_session = Seller.objects.get(email = request.session['seller_email'])
        all_product=MyOrder.objects.filter(product__seller=seller_session)
        return render(request,'seller_index.html',{'seller_data':seller_session,'order_data':all_product})
    except:
        return render(request,'seller_login.html')

def profile(request):
    return render(request,'my-profile.html')

def seller_register(request):
    if request.method =='GET':
        return render(request,'seller_register.html')
    else:
        try:
            seller_obj = Seller.objects.get(email = request.POST['s_email'])
            return render(request,'seller_register.html',{'msg':'*Email Is Already Exists!'})
        except:
            # return HttpResponse('ho gaya')  matlab yaha use object mil rhaa he
            if request.POST['password'] == request.POST['repassword']:
                global seller_dict
                seller_dict = {
                'full_name':request.POST['full_name'],
                'email'  : request.POST['s_email'],
                'password':request.POST['password'] 
                }
                global my_otp
                my_otp = random.randint(1000,9999)
                subject = 'ACCOUNT CREATION'
                message = f"HELLO {request.POST['full_name']}\n YOUR OTP IS {my_otp}"
                f_mail = settings.EMAIL_HOST_USER
                r_list = [request.POST['s_email']]
                send_mail(subject,message,f_mail,r_list)

                return render(request,'seller_otp.html',{'msg':'*check your inbox !!'})
            else:
                return render(request,'seller_register.html',{'msg':'Password is not matched!!'})

def seller_otp(request):
    if int(my_otp) == int(request.POST['s_otp']): 
        Seller.objects.create(
            full_name = seller_dict['full_name'],
            email = seller_dict['email'],
            password = seller_dict['password']

        )
        return render(request,'seller_index.html')
    else:
        return render(request,'seller_otp.html',{'msg':'Entered OTP is not matched'})

def seller_login(request):
   if request.method == 'POST':
        try:
            seller_obj = Seller.objects.get(email = request.POST['email'])
            if seller_obj.password == request.POST['password']:
                request.session['seller_email']=request.POST['email']
                # return render(request,'seller_index.html',{""})
                return redirect('seller_index')

            else:
                return render(request,'seller_login.html',{'msg':'Password is Wrong'})
        except:
            return render(request,'seller_register.html',{'msg':'Email does not Exist '})
   else:
    try:
        s_mail = request.session['seller_email']
        return redirect('seller_index')
    except:
        return render(request,'seller_login.html')


def seller_logout(request):
     del request.session['seller_email']
     return render(request,'seller_index.html')


def seller_forget(request):
    if request.method =="POST":
        try:
            seller_obj = Seller.objects.get(email = request.POST['email'])   
            subject = 'FOR GETTING PASSWORD'
            message = f"HELLO {seller_obj.full_name}\n YOUR PASSWORD IS  {seller_obj.password}"
            f_mail = settings.EMAIL_HOST_USER
            r_list = [request.POST['email']]
            send_mail(subject,message,f_mail,r_list)
            return render(request,'seller_login.html',{'msg':'*check your mail-box.'})
        except:
             return render(request,'seller_forget.html',{'msg':'Email Does not Exist'})
    else:
        return render(request,'seller_forget.html')



def seller_edit(request):
    if request.method =='POST':
        seller_obj = Seller.objects.get(email = request.session['seller_email'])
        seller_obj.full_name = request.POST['full_name']
        seller_obj.mobile =request.POST['mobile']    
        seller_obj.Pic = request.FILES['pic']
        seller_obj.save()
        return render(request,'seller_edit.html',{'seller_data' : seller_obj})
    else:
        try:
            seller_obj = Seller.objects.get(email = request.session['seller_email'])
            return render(request,'seller_edit.html',{'seller_data':seller_obj})
        except:
            return render(request,'seller_login.html',{'msg':'login please '})

def add_product(request):
    seller_obj = Seller.objects.get(email =request.session['seller_email'])
    if request.method == 'POST':
        try:
            seller_obj = Seller.objects.get(email =request.session['seller_email'])
            Product.objects.create(
                product_name = request.POST['product_name'],
                des = request.POST['des'],
                price = request.POST['price'],
                pic = request.FILES['pic'],
                seller = seller_obj
            )
            return render(request,'add_product.html',{'seller_data':seller_obj})
        except:
            return render(request,'add_product.html',{'seller_data':seller_obj})
    else:
        return render(request,'add_product.html',{'seller_data':seller_obj})


def my_products(request):
    seller_obj = Seller.objects.get(email = request.session['seller_email'])
    seller_product = Product.objects.filter(seller = seller_obj)
    return render(request,'my_products.html',{'product_data':seller_product,'seller_data':seller_obj})
  
                
        
   
def edit_product(request,pk):
    seller_obj  = Seller.objects.get(email = request.session['seller_email'])
    product_obj = Product.objects.get(id = pk)
    if request.method == 'POST':
        product_obj.product_name = request.POST['product_name']
        product_obj.des = request.POST['des']
        product_obj.price = request.POST['price']
        product_obj.pic = request.FILES['pic']
        product_obj.save()
        return render(request,'my_products.html',{'seller_data':seller_obj,'product_data':product_obj})  
    else:
        return render(request,'edit_product.html',{'seller_data':seller_obj,'product_data':product_obj})


def del_product(request,pk ):
    
        seller_obj =Seller.objects.get(email = request.session['seller_email'])
        product_obj = Product.objects.get(id = pk)
        product_obj.delete()
        return redirect('my_products')



def change_status(request,pk):
    row_obj = MyOrder.objects.get(id = pk)
    row_obj.status = 'dispatched'
    row_obj.save()
    return redirect('seller_index')


    