import random
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from seller.models import *


import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# Create your views here.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def about(request):
    return render(request,'about.html')


def contact(request):
    return render(request,'contact.html')

def faqs(request):
    return render(request,'faqs.html')

def help(request):
    return render(request,'help.html')

def index(request):
    all_product = Product.objects.all()
    try:
        s_mail = request.session['email']
        user_ka_obj = Buyer.objects.get(Email = s_mail)
        return render(request,'index.html',{'user_data': user_ka_obj,'all_product':all_product})
    except:
        return render(request,'index.html',{'all_product':all_product})

   

    return render(request,'index.html')


def payment(request):
    return render(request,'payment.html')

def privacy(request):
    return render(request,'privacy.html')

def product(request):
    return render(request,'product.html')

def product2(request):
    return render(request,'product2.html')

def single(request):
    return render(request,'single.html')

def single2(request):
    return render(request,'single2.html')

def terms(request):
    return render (request,'terms.html')

def add_row(request):
    Buyer.objects.create(
        First_name  ='vijay',
        Last_name   ='Bokade',
        Email       ='looserbokade26@gmail.com',
        Password    = '13325'  ,
        Address     ='23, maa gayatri krupa society'
    )
    return render(request,'add_row.html')

def del_row(request):
     user_row = Buyer.objects.get(Email = 'vijaybokade26@gmail.com')
     user_row.delete()
     return HttpResponse('delete a row')


def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        try:
            Buyer.objects.get(Email = request.POST['email'])
            return render(request,'register.html',{'msg':'Email is already exist!!'})
        except ObjectDoesNotExist:
            if request.POST['password'] == request.POST['repassword']:
                # return HttpResponse('bhai tu jaa sakta he ')
                        
                        
                global c_otp
                c_otp = random.randint(10000,99999)
                subject = 'Account Activation.'
                message = f"Hello {request.POST['firstname']}.\n Your OTP is {c_otp}"
                f_mail = settings.EMAIL_HOST_USER
                r_list = [request.POST['email']]

                global user_dict
                user_dict = {
                'firstname':request.POST['firstname'],
                'lastname':request.POST['lastname'],
                'email'  : request.POST['email'],
                'password':request.POST['password'] 
                }

                send_mail(subject,message,f_mail,r_list)
                return render(request,'otp.html',{'msg':'---check your inbox !!'})

            else:
                # return HttpResponse('bhai passowrd to sahi daal')
                return render(request,'register.html',{'msg':'---password is not matched.'})

def otp(request):
    if int(c_otp) == int(request.POST['u_otp']):
        Buyer.objects.create(
            First_name = user_dict['firstname'],
            Last_name = user_dict['lastname'],
            Email = user_dict['email'],
            Password = user_dict['password']

        )
        # return HttpResponse('ho gaya')
        return render(request,'index.html')
    else:
        return render(request,'otp.html',{'msg':'bhai otp to sahi daal'})


def login(request):
    if request.method  == 'POST':
        try:
            user_ka_obj = Buyer.objects.get(Email = request.POST['email'])
            # hum email chek krenge ki post metod se jo email aa rha 
            # he wo database mejo mail he us se match hota he k nhi
            if user_ka_obj.Password == request.POST['password']:
                request.session['email'] = request.POST['email']
                return redirect('index')
            else:
                 return render(request,'login.html',{'msg':'password is wrong'})
        except:
            return render(request,'register.html',{'msg': 'email does not exist!'})
    else:
        try:
            request.session['email']
            return redirect('index')
        except:
            return render(request,'login.html')

def logout(request):
    del request.session['email']
    return render(request,'index.html')


def forget(request): 
    if request.method =='POST':
       try:
            user_obj =  Buyer.objects.get(Email =request.POST['email'])
            subject = 'For Getting Password'
            message = f'Hello  {user_obj.First_name}\nYour Psassword is {user_obj.Password}'
            f_email = settings.EMAIL_HOST_USER
            r_list = [user_obj.Email]
            send_mail(subject,message,f_email,r_list)
            return render(request,'login.html',{'msg':'Check Your Mail-Box.'})
       except:
            return render(request,'forget.html',{'msg':"Entered Email Doesn't Exist!!"})
    else:
        return render(request,'forget.html')


def edit_profile(request):
    if request.method == "GET":#get method se sirf session chalu he k nhi vo btayega 
        try:
            user_obj = Buyer.objects.get(Email =request.session['email'])
            #agar database me jo email he or jis email ka session chalu he vo email match ho gya to 
            # hum use edit profile pr bhejenge data k sath
            return render(request,'edit_profile.html',{'user_data':user_obj})
        except:
            return render(request,'login.html') 
    else:#post method se hum jo bhi data edit kr k save krenge vo btayega
       user_row =  Buyer.objects.get(Email = request.session['email'])
       user_row.First_name = request.POST['firstname']
       user_row.Last_name = request.POST['lastname']
       user_row.Address =request.POST['address']
       user_row.Phone =request.POST['phone']    
       user_row.Pic = request.FILES['pic']
       user_row.save()
       return render(request,'edit_profile.html',{'user_data':user_row})
       #image icon dekhne k liye sabse pehle media ka folder bnao 
    #    fir settings.py me jaa ke media ko register kro
#     MEDIA_URL = '/media/'
#     MEDIA_ROOT = os.path.join(BASE_DIR, 'media')===.write this.

def reset(request):
    if request.method == 'POST':
        try:
            user_session = Buyer.objects.get(Email = request.session['email'])
            try:
                user_pass = Buyer.objects.get(password =request.POST['o_password'])
                request.POST['n_password'] == request.POST['re_password']
                user_pass.save()
                return HttpResponse('ho gya')
            except:
                return render(request,'reset.html',{'msg':'Entered Password Is Wrong'})
                
        except:
            return render(request,'login.html')
            
    else:
        return render(request,'reset.html')

def add_to_cart(request,pk):
    all_product = Product.objects.all()
    buyer_obj = Buyer.objects.get(Email = request.session['email'])
    product_obj = Product.objects.get(id = pk)
    Cart.objects.create(
        buyer = buyer_obj,
        product = product_obj
    )
    return render(request,'index.html',{'user_data': buyer_obj,'all_product':all_product})


# def checkout(request):
#     user_obj = Buyer.objects.get(Email = request.session['email'])
#     cart_list = Cart.objects.filter(buyer=user_obj)
#     total_price = 0
#     for i in cart_list:
#         total_price += (i.product.price)
#     return render(request,'checkout.html',{'cart_list':cart_list,'user_data':user_obj,'total_price':total_price})

def del_cart_row(request, pk):
    del_row = Cart.objects.get(id = pk)
    del_row.delete()
    return redirect('checkout')





def checkout(request):
    s_email = (request.session).get('email')
    if not s_email:
        return render(request, 'login.html')
    user_data = Buyer.objects.get(Email = s_email)
    cart_list = Cart.objects.filter(buyer = user_data)
    total_price = 0
    for i in cart_list:
        total_price += i.product.price
    total_price *= 100 
    currency = 'INR'
    global amount
    amount = int(total_price) # Rs. 200
    if amount == 0:
        amount = 100 #because 100 paise barabar ek rupaiya hota hai
    
    
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
													currency=currency,
													payment_capture='0'))

	# order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

	# we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['user_data'] = user_data
    context['cart_list'] = cart_list
    context['total_price'] = total_price
    context['rupee_total_price'] = total_price / 100

    return render(request, 'checkout.html', context=context)


@csrf_exempt
def paymenthandler(request):

    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
                }
            global amount
            amount = amount
            try:
                razorpay_client.payment.capture(payment_id, amount)
                session_user = Buyer.objects.get(Email = request.session['email'])
                c_objects_list = Cart.objects.filter(buyer = session_user)
                for i in c_objects_list:
                    MyOrder.objects.create(
                        buyer = session_user,
                        product = i.product,
                        status = 'pending'
                    )
                    i.delete()
                
                return render(request, 'paymentsuccess.html')
            except:
                return render(request, 'paymentfail.html')
           
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()



         

            
        