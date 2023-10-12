import requests
import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm, SignupForm, SignupFormextra, ContactUsForm, ContactForm, SubscriberForm, UserMessageForm
from .models import UserExtraInformation,UserMessages,Contact,subscriber
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
import datetime
import time
from django.contrib import messages

from django.views import View 
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator

# Create your views here.

def userlogin(request):
    """
    A functional based view for the login page (login.html)
    """
    message=""
    if request.method =='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                message="user found"
                login(request, user)
                return redirect('../profile/')
            elif user is None:
                print(user)
                message="Invalid Login Details"                                        
                return render (request, "argon/login.html", {'form':form,'message':message})
    else:
        form=LoginForm()
    return render (request, "argon/login.html", {'form':form,'message':message})

def userlogout(request):
    logout(request)
    return redirect('../login/')       
               
def signup(request):
    """
    A functional based view for the signup page (register.html)
    """

    message=""
    if request.method=='POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            lastname = form.cleaned_data['lastname']
            firstname = form.cleaned_data['firstname']
            try:
                if User.objects.filter(email=email).exists():
                   message = "Email address used on another account."
                   return render (request, "argon/register.html", {'form':form,'message':message})
                user = User.objects.create_user(username, email, password)
                
            except:
                message = "invalid data, username might be taken. try changing username"
                return render (request, "argon/register.html", {'form':form,'message':message})
            
            
            
            if user is not None:
                message="Congratulations!!!\n You have successfully created an account! Login to complete the registration process."
                user.last_name = lastname
                user.first_name = firstname
                user.save()
                
                uidb64 = force_str(urlsafe_base64_encode(force_bytes(str(user.pk))))

                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={"uidb64":uidb64, "token":token_generator.make_token(user)})
                
                activate_url = "https://"+domain+link #use https for development


                email_subject = 'Activate your account'
                email_body ="Hi, " + user.username + " \n \n Your Ccryptogram account has been successfully Activated. \n Welcome to ccryptogram.\n motto: Give back to the people \n activate Your account by clicling the link below. \n " + activate_url + " \n \n for investment or enquires, contact \n - any senior broker at ccryptograminc \n "
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'ccryptograminconline@gmail.com',
                    [user.email],

                )
            
                email.send(fail_silently=True)
                if user.is_active:
                    return redirect('../signupextra/')
                
            else:
                message="username or password can't be used "
                pass      
    else:
        form=SignupForm()
    
    return render (request, "argon/register.html", {'form':form,'message':message})



class VerificationView(View):
    def get(self, request, uidb64, token):
        # try:
            
            id = force_text(urlsafe_base64_decode(uidb64))
            
            user = User.objects.get(pk = id)
            
            
            if user.is_active:
                try:
                    UserExtraInformation.objects.get(user=user)
                    return redirect("profile")
                except:
                    return redirect("signupextra")
                
            else:
                user.is_active = True
                user.save()
                return redirect("login")
        
            return redirect ("signup")    


@login_required(login_url='/login/')
def signupextra(request):
    """
    A functional based view for capturing the user's extra data
    """

    message=""
    if request.method=='POST':
        form = SignupFormextra(request.POST)
        if form.is_valid():
            moblie_number = form.cleaned_data['moblie_number']
            occupation = form.cleaned_data['occupation']
            alternate_email = form.cleaned_data['alternate_email']
            country = form.cleaned_data['country']
            wallet_address = form.cleaned_data['wallet_address']
            date_of_birth = form.cleaned_data['date_of_birth']
           
            if not UserExtraInformation.objects.filter(user=request.user).exists():
                UserExtraInformation.objects.create(
                user=request.user,
                country=country,
                moblie_number=moblie_number,
                occupation=occupation, 
                alternate_email=alternate_email,
                wallet_address=wallet_address,
                date_of_birth=date_of_birth,
                
                balance=0,
                amount_withdrawable=0,
                amount_available=0,)
                return redirect('../profile')
            else:
                return redirect("profile")
        else:
            message="invalid form"
            return render (request, "argon/register.html", {'form':form,'message':message})        
    else:
        form=SignupFormextra()
    return render (request, "argon/register.html", {'form':form,'message':message})


@login_required(login_url='/login/')
def profile(request):
    """
    A functional based view for the profile page (profile.html)
    """

    try:
        UserExtraInformation.objects.get(user=request.user)
    except:
        return redirect("signupextra")
    user = User.objects.get(username=request.user)
    information = UserExtraInformation.objects.get(user=request.user)  
    message = UserMessages.objects.filter(sender=request.user)
    message_count = len(message)

    try:
        bitcoin = data.getprices("bitcoin","usd")
        bitcoineur = data.getprices("bitcoin","eur")
        ethereum = data.getprices("ethereum","usd")
        bitcoincash = data.getprices("bitcoin-cash","usd")
        ripple = data.getprices("ripple","usd")
        elitecoin = data.getprices("elitecoin","usd")
        cardano = data.getprices("cardano","usd")
        nem = data.getprices("nem","usd")
        bitcoinneo = data.getprices("bitcoin-neo","usd")
        iota = data.getprices("iota","usd")
        gold = information.gold
    except:
        bitcoin = ""
        bitcoineur = ""
        ethereum = ""
        bitcoincash = ""
        ripple = ""
        elitecoin = ""
        cardano = ""
        nem = ""
        bitcoinneo = ""
        iota = ""
        gold = ""
        

    if request.method=='POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            sender=request.user
            UserMessages.objects.create(
                sender=sender,
                email=sender.email,
                message = message,
                subject = "customer service"
            )
    else:
        form = ContactUsForm()
    return render(request, "argon/dashboard.html",{'form':form, 'user':user, 'information':information, 'message':message, 'message_count':message_count,'bitcoineur':bitcoineur,'ethereum':ethereum, 'bitcoincash':bitcoincash, 'ripple':ripple, 'elitecoin':elitecoin, 'cardano':cardano, 'nem':nem, 'bitcoinneo':bitcoinneo, 'gold':gold })

@login_required(login_url='/login/')
def detail(request):
    """
    A functional based view for the detail page (details.html)
    """

    user = User.objects.get(username=request.user)
    information = UserExtraInformation.objects.get(user=request.user)  
    message = UserMessages.objects.filter(sender=request.user)
    message_count = len(message)
    try:
        bitcoin = data.getprices("bitcoin","usd")
    except:
         bitcoin = ""

    if request.method=='POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            sender=request.user
            UserMessages.objects.create(
                sender=sender,
                email=sender.email,
                message = message,
                subject = "customer service"
            )
    else:
        form = ContactUsForm()
    return render(request, "argon/profile.html",{'form':form, 'user':user, 'information':information, 'message':message, 'message_count':message_count,  })

class data():
    def getprices(coin,currency):
        URL = "https://api.coingecko.com/api/v3/simple/price?ids="+coin+"&vs_currencies="+currency+"%2C%20eth&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true"
        r = requests.get(url = URL)
        data = r.json()
        return (data[coin][currency])
        pass

def error(request):

     return render (request, "404.html")

def index(request):
    """
    A functional based view for the index page (index_main.html)
    """

    form = SubscriberForm(request.POST)
    
    try:
        bitcoin = data.getprices("bitcoin","usd")
        bitcoineur = data.getprices("bitcoin","eur")
        ethereum = data.getprices("ethereum","usd")
        bitcoincash = data.getprices("bitcoin-cash","usd")
        ripple = data.getprices("ripple","usd")
        elitecoin = data.getprices("elitecoin","usd")
        cardano = data.getprices("cardano","usd")
        nem = data.getprices("nem","usd")
        bitcoinneo = data.getprices("bitcoin-neo","usd")
        iota = data.getprices("iota","usd")

    except:
        bitcoin = ""
        bitcoineur = ""
        ethereum = ""
        bitcoincash = ""
        ripple = ""
        elitecoin = ""
        cardano = ""
        nem = ""
        bitcoinneo = ""
        iota = ""
   
    if request.method=='POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
        if form1.is_valid():
            message = form1.cleaned_data['message']
            name = form1.cleaned_data['name']
            email = form1.cleaned_data['email']
            Contact.objects.create(
                name=name,
                email=email,
                message = message,
                subject = "Requested a call back"
            )
        message="Message sent to our team"       
        subscriber.objects.create(
                
                email=email,
               
            )
    else:
        form1 = ContactForm()
        
        message="send message to our service team"
        form = SubscriberForm()

    return render (request, "coinbuzz/index_main.html", {'bitcoin':bitcoin,'bitcoineur':bitcoineur,'ethereum':ethereum, 'bitcoincash':bitcoincash, 'ripple':ripple, 'elitecoin':elitecoin, 'cardano':cardano, 'nem':nem, 'bitcoinneo':bitcoinneo, 'iota':iota,'form':form, 'form1':form1})


def contact(request):
    """
    A functiomal based view for the contact.html page
    """
    
    message = ""

    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        form1 = ContactForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']

        if form1.is_valid():
            print("form is valid")
            message = form1.cleaned_data['message']
            name = form1.cleaned_data['name']
            email = form1.cleaned_data['email']
            contact_form = Contact.objects.create(
                name=name,
                email=email,
                message = message,
                subject = "contact form"
            )
            
            subscriber.objects.create(
                
                email=email,
               
            )
            contact_form.save()
        message="Message sent to our team"
        return render (request, "coinbuzz/index_main.html", {'form':form,'form1':form1, 'message':message})
    else:
        form1 = ContactForm()
        form = SubscriberForm()
        message="send message to our service team"
    return render (request, "coinbuzz/contact.html", {'form':form,'form1':form1, 'message':message})

def about(request):
    """
    A functional based view for the about page (about.html)
    """

    if request.method=='POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            new_subscriber = subscriber.objects.create(
                
                email=email,
               
            )
            new_subscriber.save()
    else:
        form = SubscriberForm()
    return render (request, "coinbuzz/about.html", {'form':form})

def faq(request):
    """
    A functional based view for the faq page (faq.html)
    """

    form = SubscriberForm(request.POST)
    if request.method=='POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            new_subscriber = subscriber.objects.create(
                
                email=email,
               
            )
        else:
            form = SubscriberForm()
    return render (request, "coinbuzz/faq.html", {'form':form})



def testimony(request):
    """
    A functional based view for the testimonial page (testimony.html)
    """

    form = SubscriberForm(request.POST)
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            new_subscriber = subscriber.objects.create(
                
                email=email,
               
            )
            new_subscriber.save()
    else:
        form = SubscriberForm()
    return render (request, "coinbuzz/testimony.html", {'form':form})

def blog(request):
     return render (request, "cryptos/blog.html")

@login_required(login_url='/login/')
def withdraw(request):
    """
    A functional based view for the withdraw page (withdraw.html)
    """

    user = User.objects.get(username=request.user)
    information = UserExtraInformation.objects.get(user=request.user)  
    message = UserMessages.objects.filter(sender=request.user)
    message_count = len(message)
    transaction_form =  UserMessageForm(request.POST)
    form = ContactUsForm()

    try:
        bitcoin = data.getprices("bitcoin","usd")
        bitcoineur = data.getprices("bitcoin","eur")
        ethereum = data.getprices("ethereum","usd")
        bitcoincash = data.getprices("bitcoin-cash","usd")
        ripple = data.getprices("ripple","usd")
        elitecoin = data.getprices("elitecoin","usd")
        cardano = data.getprices("cardano","usd")
        nem = data.getprices("nem","usd")
        bitcoinneo = data.getprices("bitcoin-neo","usd")
        iota = data.getprices("iota","usd")
        gold = information.gold
    except:
        bitcoin = ""
        bitcoineur = ""
        ethereum = ""
        bitcoincash = ""
        ripple = ""
        elitecoin = ""
        cardano = ""
        nem = ""
        bitcoinneo = ""
        iota = ""
        gold = ""
    

    if request.method == 'POST':
        form = ContactUsForm()
        if transaction_form.is_valid():
            message = transaction_form.cleaned_data['message']
            transaction_amount = transaction_form.cleaned_data['Transaction_Amount']
            wallet_address = transaction_form.cleaned_data['wallet_address']
            sender=request.user
            Withdrawal_Request = UserMessages.objects.create(
                sender=sender,
                email=sender.email,
                wallet_address=wallet_address,
                Transaction_Amount = transaction_amount,
                message = message,
                subject = "Pending Deposit Request",
            )
            Withdrawal_Request.save()
    else:
        form = ContactUsForm()
    return render(request, "argon/withdraw.html",{'form':form, 'withdrawal_form':transaction_form, 'user':user, 'information':information, 'message':message, 'message_count':message_count, 'bitcoin':bitcoin,'bitcoineur':bitcoineur,'ethereum':ethereum, 'bitcoincash':bitcoincash, 'ripple':ripple, 'elitecoin':elitecoin, 'cardano':cardano, 'nem':nem, 'bitcoinneo':bitcoinneo, 'iota':iota, 'gold':gold })

def test(request):
     return render (request, "argon/test.html")



@login_required(login_url='/login/')
def deposit(request):
    """
    A functional based view for the withdraw page (withdraw.html)
    """

    user = User.objects.get(username=request.user)
    information = UserExtraInformation.objects.get(user=request.user)  
    message = UserMessages.objects.filter(sender=request.user)
    message_count = len(message)
    transaction_form =  UserMessageForm(request.POST)
    form = ContactUsForm()

    try:
        bitcoin = data.getprices("bitcoin","usd")
        bitcoineur = data.getprices("bitcoin","eur")
        ethereum = data.getprices("ethereum","usd")
        bitcoincash = data.getprices("bitcoin-cash","usd")
        ripple = data.getprices("ripple","usd")
        elitecoin = data.getprices("elitecoin","usd")
        cardano = data.getprices("cardano","usd")
        nem = data.getprices("nem","usd")
        bitcoinneo = data.getprices("bitcoin-neo","usd")
        iota = data.getprices("iota","usd")
        gold = information.gold
    except:
        bitcoin = ""
        bitcoineur = ""
        ethereum = ""
        bitcoincash = ""
        ripple = ""
        elitecoin = ""
        cardano = ""
        nem = ""
        bitcoinneo = ""
        iota = ""
        gold = ""

    

    if request.method == 'POST':
        form = ContactUsForm()
        if transaction_form.is_valid():
            message = transaction_form.cleaned_data['message']
            transaction_amount = transaction_form.cleaned_data['Transaction_Amount']
            sender=request.user
            new_deposit = UserMessages.objects.create(
                sender=sender,
                email=sender.email,
                Transaction_Amount = transaction_amount,
                message = message,
                subject = "Pending Deposit Request",
            )
            new_deposit.save()

    else:
        form = ContactUsForm()
    return render(request, "argon/deposit.html",{'form':form, 'user':user, 'form2':transaction_form, 'information':information, 'message':message, 'message_count':message_count, 'bitcoin':bitcoin,'bitcoineur':bitcoineur,'ethereum':ethereum, 'bitcoincash':bitcoincash, 'ripple':ripple, 'elitecoin':elitecoin, 'cardano':cardano, 'nem':nem, 'bitcoinneo':bitcoinneo, 'iota':iota, 'gold':gold })


