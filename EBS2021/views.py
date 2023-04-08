from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from datetime import date
import uuid
import json
import logging as log
from django.http import JsonResponse
from decimal import Decimal
from decimal import getcontext
import re
import datetime


from django.shortcuts import render
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
import requests as rq

# Create your views here.
def index(request):
    return render(request ,"index.html")

def Login(request):
    error=""
    if request.method=='POST':
        u=request.POST['uname']
        p=request.POST['password']
        user=authenticate(username=u,password=p)
        if user:
            try:
                if user.is_authenticated:
                    login(request,user)
                    error="no"
                else:
                    error="yes"
            except:
                error="yes"                   
    d = {'error':error}
    return render(request,"login.html",d)

def Userlogin(request):
    error=""
    if request.method=='POST':
        e=request.POST['email']
        p=request.POST['pwd']
        user=authenticate(username=e,password=p)
        if user:
            try:
                user1 = UserSignup.objects.get(user=user)
                if user1:
                    login(request,user)
                    error="no"
                else:
                    error="yes"
            except:
                error="yes"
        else:
            error="yes"                    
    d = {'error':error}
    return render(request,'userlogin.html',d)    

def change_passworduser(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    error=""    
    if request.method=="POST":
        c= request.POST['currentpassword']
        n= request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
               u.set_password(n) 
               u.save()
               error="no"
            else:
               error="not"   
        except:
            error="yes"    
    d={"error":error}   
    return render(request,"changepassworduser.html",d) 

def userhome(request):
    if not request.user.is_authenticated:
        return redirect('Userlogin')
    user = request.user 
    data = UserSignup.objects.get(user=user)
    error=""
    if request.method=='POST':
        con=request.POST['contact']
        fn=request.POST['fname']
        ln=request.POST['lname']
        address = request.POST['address']

        data.mobile = con
        data.user.first_name = fn
        data.user.last_name = ln
        data.address = address
        try:
            data.save()
            data.user.save()
            error="no"
        except:
            error="yes" 
        try:
            i=request.FILES['image']
            data.image = i
            data.save()
            error="no"
        except:
            pass
    d ={"data":data,'error':error}   
    return render(request ,"userhome.html",d)

def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('Login')
    error=""    
    if request.method=="POST":
        c= request.POST['currentpassword']
        n= request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
               u.set_password(n) 
               u.save()
               error="no"
            else:
               error="not"   
        except:
            error="yes"    
    d={"error":error}   
    return render(request,"changepassword_admin.html",d) 


def add_event(request):
    if not request.user.is_authenticated:
        return redirect('Login')
    error = ""
    category = Category.objects.all()
    if request.method=='POST':
        en=request.POST['ename']
        i=request.FILES['image']
        cat=request.POST['category']
        des=request.POST['description']
        #sd=request.POST['startdate']
        #ed=request.POST['enddate']
        ve=request.POST['venue']
        ep=request.POST['price']

        try:
           #Event.objects.create(eventname=en,image=i,category=cat,description=des,startdate=sd,enddate=ed,venue=ve,entryprice=ep)
           Event.objects.create(eventname=en,image=i,category=cat,description=des,venue=ve,entryprice=ep)
           error="no"
        except:
           error="yes"

    return render(request ,"add_event.html",locals())


def edit_event(request,pid):
    if not request.user.is_authenticated:
        return redirect('Login')
    error = ""
    category = Category.objects.all()
    event = Event.objects.get(id=pid)
    if request.method=='POST':
        en=request.POST['ename']

        cat=request.POST['category']
        des=request.POST['description']

        ve=request.POST['venue']
        ep=request.POST['price']
        event.eventname = en
        event.category=cat
        event.description=des
        event.venue=ve
        event.entryprice=ep

        try:
           event.save()
           error="no"
        except:
           error="yes"
        try:
            i=request.FILES['image']
            event.image = i
            event.save()
        except:
            pass
        try:
            startdate = request.POST['startdate']
            event.startdate = startdate
            event.save()
        except:
            pass
        try:
            enddate = request.POST['enddate']
            event.enddate = enddate
            event.save()
        except:
            pass
    return render(request ,"edit_event.html",locals())


def view_event(request):
    if not request.user.is_authenticated:
        return redirect('Login')
    event = Event.objects.all()
    d = {'event':event}    
    return render(request ,"view_event.html",d)

def view_details(request,pid):
    if not request.user.is_authenticated:
        return redirect('userLogin')  
    data= Event.objects.get(id=pid)
    sponsor = SponsorTbl.objects.filter(event=data)
    return render(request ,"details.html",locals())

def view_eventuser(request):
    if not request.user.is_authenticated:
        return redirect('userLogin')
    event = Event.objects.all()
    d = {'event':event}    
    return render(request ,"view_eventuser.html",d)     

def delete_event(request,pid):
      if not request.user.is_authenticated:
        return redirect('Login')
      apoint= Event.objects.get(id=pid)
      apoint.delete()
      return redirect('view_event')

def add_sponsor(request):
    if not request.user.is_authenticated:
        return redirect('Login')
    error = ""
    event1=Event.objects.all()
    if request.method=='POST':
        eventid=request.POST['event']
        i=request.FILES['image']
        event = Event.objects.get(id = eventid)
        try:
           SponsorTbl.objects.create(event=event,sponsorimage=i)
           error="no"
        except:
            error="yes"
    d = {'event1':event1,'error':error}    
    return render(request ,"add_sponsor.html",d)

def view_sponsor(request):
    if not request.user.is_authenticated:
        return redirect('Login')
    sponsor = SponsorTbl.objects.all()
    d = {'sponsor':sponsor}    
    return render(request ,"view_sponsor.html",d) 

def delete_sponsor(request,pid):
      if not request.user.is_authenticated:
        return redirect('Login')
      apoint= SponsorTbl.objects.get(id=pid)
      apoint.delete()
      return redirect('view_sponsor')

def add_category(request):
    if not request.user.is_authenticated:
        return redirect('Login')
    error = ""
    if request.method=='POST':
        cn=request.POST['cname']
        try:
           Category.objects.create(categoryname=cn)
           error="no"
        except:
            error="yes"
    d = {'error':error}    
    return render(request ,"add_category.html",d)

def view_category(request):
    if not request.user.is_authenticated:
        return redirect('Login')
    cat = Category.objects.all()
    d = {'cat':cat}    
    return render(request ,"view_category.html",d) 

def delete_category(request,pid):
      if not request.user.is_authenticated:
        return redirect('Login')
      apoint= Category.objects.get(id=pid)
      apoint.delete()
      return redirect('view_category')

def view_user(request):
    if not request.user.is_authenticated:
        return redirect('Login')
    user1 = UserSignup.objects.all()
    d = {'user1':user1}    
    return render(request ,"view_user.html",d)

def delete_user(request,pid):
      if not request.user.is_authenticated:
        return redirect('Login')
      apoint= UserSignup.objects.get(id=pid)
      apoint.delete()
      return redirect('view_user')

def delete_booking(request,pid):
      if not request.user.is_authenticated:
        return redirect('Login')
      apoint= Booking.objects.get(id=pid)
      apoint.delete()
      return redirect('view_mybooking')

def about(request):
    return render(request ,"about.html")


def usersignup(request):
    error=""
    if request.method=='POST':
        fn=request.POST['fname']
        ln = request.POST['lname']
        pas=request.POST['pwd']
        em=request.POST['email']
        con=request.POST['contact']
        address = request.POST['address']
        i=request.FILES['image']

        try:
            user = User.objects.create_user(username=em,password=pas,first_name=fn,last_name=ln)
            UserSignup.objects.create(user=user,mobile=con,image=i,address=address)
            error="no"
        except Exception as e:
            error="yes" 
            log.warning('Error--------->',e)
    d = {'error':error}        
    return render(request,'usersignup.html',d) 

def Logout(request):
    if not request.user.is_authenticated:
        return redirect('Login')
    logout(request)
    return render(request,"index.html")

def book_now(request,pid):
    log.warning('<------Inside Book_now---------->')
    if not request.user.is_authenticated:
        return redirect('userlogin')
    error = ""
    event1=Event.objects.get(id=pid)
    user = request.user
    userinfo = UserSignup.objects.get(user=user)
    if request.method=='POST':
        p=request.POST['person']
        t=request.POST['total']
        try:
            
           Booking.objects.create(userinfo = userinfo,eventinfo=event1,person=p,total=t,status="pending",bookingdate=date.today())
           error="no"
           log.warning('<------Booking created---------->')
           flg = sentmsg(email='abc',msgSubj='Booking Confirmation',msg='Your booking has been confirmed')
           if flg:
               log.warning('---------Message sent--------')
           else:
               log.warning('-------Unable to sent Message-------')
        except:
           error="yes"
    d = {'event1':event1,'error':error}    
    return render(request ,"book_now.html",d)

def view_mybooking(request):
    if not request.user.is_authenticated:
        return redirect('userLogin')
    user = request.user
    userinfo = UserSignup.objects.get(user=user)
    b = Booking.objects.filter(userinfo = userinfo)
    d = {'b':b}    
    return render(request ,"view_mybooking.html",d)


def bookingdetail_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('userLogin')
    booking = Booking.objects.get(id=pid)
    return render(request, 'bookingdetail_user.html', locals())



def bookingdetail_admin(request,pid):
    if not request.user.is_authenticated:
        return redirect('userLogin')
    booking = Booking.objects.get(id=pid)
    error = ""
    if request.method == "POST":
        status = request.POST['status']
        try:
            booking.status = status
            booking.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'bookingdetail_admin.html', locals())




def booking_request(request):
    if not request.user.is_authenticated:
        return redirect('Login')
    b = Booking.objects.filter(status="pending")
    return render(request ,"booking_request.html",locals())

def accepted_booking(request):
    if not request.user.is_authenticated:
        return redirect('Login')
    b = Booking.objects.filter(status="Accept")
    return render(request ,"accepted_booking.html",locals())

def rejected_booking(request):
    if not request.user.is_authenticated:
        return redirect('Login')
    b = Booking.objects.filter(status="Reject")
    return render(request ,"rejected_booking.html",locals())


def all_booking(request):
    if not request.user.is_authenticated:
        return redirect('Login')
    b = Booking.objects.all()
    return render(request ,"all_booking.html",locals())

def confirmed_booking(request):
    if not request.user.is_authenticated:
        return redirect('Login')
    b = Booking.objects.filter(status="Confirmed(Paid)")
    return render(request ,"confirmed_booking.html",locals())


def contact(request):
    return render(request ,"contact.html")

def innerhome(request):
    if not request.user.is_authenticated:
        return redirect('Login')
    totalevents = Event.objects.all().count()
    totalsponsor = SponsorTbl.objects.all().count()
    totalcategory = Category.objects.all().count()
    totalnewbooking = Booking.objects.filter(status="pending").count()
    totalconfirmbooking = Booking.objects.filter(status="Confirmed(Paid)").count()
    allbooking = Booking.objects.all().count()
    totalusers = UserSignup.objects.all().count()
    return render(request ,"innerhome.html",locals())

def edit_sponsor(request,pid):
    if not request.user.is_authenticated:
        return redirect('Login')
    error = ""
    event1=Event.objects.all()
    sponsor = SponsorTbl.objects.get(id=pid)
    if request.method=='POST':
        eventid=request.POST['event']
        event = Event.objects.get(id = eventid)
        sponsor.event = event
        try:
           sponsor.save()
           error="no"
        except:
            error="yes"
        try:
            i=request.FILES['image']
            sponsor.sponsorimage = i
            sponsor.save()
        except:
            pass
    return render(request ,"edit_sponsor.html",locals())

def edit_category(request,pid):
    if not request.user.is_authenticated:
        return redirect('Login')
    error = ""
    category = Category.objects.get(id=pid)
    if request.method=='POST':
        cn=request.POST['cname']
        try:
           category.categoryname= cn
           category.save()
           error="no"
        except:
           error="yes"
    return render(request ,"edit_category.html",locals())


def payment(request,pid):
    if not request.user.is_authenticated:
        return redirect('userLogin')
    booking = Booking.objects.get(id=pid)
    error = ""
    if request.method == "POST":
        cardnumber = request.POST['cardnumber']
        cardex = request.POST['cardex']
        cvv = request.POST['cvv']
        try:
            booking.cardno = cardnumber
            booking.expirydate = cardex
            booking.cvv = cvv
            booking.status = "Confirmed(Paid)"
            booking.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'payment.html', locals())

#@api
def paymentApi(request):
    
    print('Inside API')
        # e=request.POST['email']
        # p=request.POST['pwd']
        # user=authenticate(username=e,password=p)
    if request.method == 'POST':
        try:
            
            username=request.json['email']
            password=request.json['pwd']
            user=authenticate(username=username,password=password)
            
            if user:        
                userinfo = UserPayment()
                card_num = request.json['CARD_NUMBER']
                card_holder = request.json['CARD_HOLDER']
                cardDate = request.json['END_DATE']
                security_code = request.json['CVV']
                amount = request.json['AMT']
                amount = float(amount)
                card_num = card_num.strip().replace(" ","")
                card_num_len = len(card_num)
                card_holder = card_holder.strip().upper()
                security_code = str(security_code)
                dateObj = datetime.datetime.strptime(cardDate,'%m/%Y')
                expiry_date = dateObj.date()
        
                respMsg,respCode = cardValidation(card_num,card_holder,expiry_date,security_code,amount,card_num_len)
                
                cur_date = datetime.datetime.now()
                tx_id = uuid.uuid4()
                
                userinfo.cardNumber = card_num
                userinfo.cardHolder = card_holder
                userinfo.expiryDate = expiry_date
                userinfo.userName = username
                userinfo.transactionAmt = int(amount)
                userinfo.transactionId = tx_id
                userinfo.transactionDate = cur_date
                
                try:
                    log.warning('<-----------Saving data--------->')
                    userinfo.save()
                    return  JsonResponse({'RESPONSE_MSG': respMsg,'RESPONSE_CODE':respCode,'DATE_TIME':str(cur_date),'TRANSACTION_ID': str(tx_id)})
                except Exception as ex:
                    log.warning('Error--------------->',ex)
                    return  JsonResponse({'RESPONSE_MSG': 'Internal Error','RESPONSE_CODE':500,'DATE_TIME':str(cur_date)})
                    
            else:
                log.warning('INVALID USER',)
                cur_date = datetime.datetime.now()
                respMsg = 'Invalid User'
                return  JsonResponse({'RESPONSE_MSG': respMsg,'RESPONSE_CODE':400,'DATE_TIME':str(cur_date)})
            
        
        except Exception as e:
            log.warning('Error------------->',e)
            cur_date = datetime.datetime.now()
            respMsg = 'The request is invalid'
            return  JsonResponse({'RESPONSE_MSG': respMsg,'RESPONSE_CODE':400,'DATE_TIME':str(cur_date)})
            


    return None        




def cardValidation(card_num,card_holder,expiry_date,security_code,amount,card_num_len):

    try:

        if card_num_len in [13,15,16] and card_num.isdigit():
            # Visa Card
            if (card_num_len == 13 or card_num_len == 16) and card_num.startswith('4'):
                pass
            # Mastercard
            elif card_num_len == 16 and card_num.startswith('5'):
                pass
            # AMEX
            elif card_num_len == 15 and (card_num.startswith('34') or card_num.startswith('37')):
                pass
            # Discover
            elif card_num_len == 16 and card_num.startswith('6'):
                pass
            else:
                log.warning("Invalid Card Number\n")
                return 'The request is invalid', 400
        else:
            log.warning("Invalid Card Number: {}\n".format(card_num))
            return 'The request is invalid', 400

        card_num = int(card_num)

        log.warning("Passed Card Num check")

        if len(card_holder) > 4:

            verify_name = bool(re.match(r'^[A-Z]{2,24} [A-Z]{2,24}$', card_holder))
            log.warning("Card Holder ({}) Verified: {}".format(card_holder,verify_name))

            if not verify_name:
                log.warning("Card Holder Value Invalid!\n")
                return 'The request is invalid', 400
            else:
                log.warning("Valid Card Holder")

        else:
            log.warning("Card Holder Value Invalid!\n")
            return 'The request is invalid', 400


        if type(expiry_date) is not datetime.date:

            log.warning("Invalid Expiry Date: {}\n".format(expiry_date))
            # bad request
            return 'The request is invalid', 400
        
        if expiry_date <= datetime.date.today():
            
            log.warning("Invalid Expiry Date: {}\n".format(expiry_date))
            # bad request
            return 'The request is invalid', 400
        
            




        getcontext().prec = 8


        if bool(re.match(r'^[0-9]{1,6}\.[0-9]{1,2}$', str(amount))):
            amount = Decimal(amount).quantize(Decimal('1.00'))
            log.warning("Amount valid: {}".format(str(amount)))
        else:
            log.warning("Amount Invalid: {}\n".format(str(amount)))
            # bad request
            return 'The request is invalid', 400


        if security_code != "":

            security_str = str(security_code).strip()

            if security_str.isdigit() and len(security_str) == 3:
                log.warning("Valid Security Code")
                security_code = int(security_code)
            else:
                log.warning("Invalid Security Code: {}\n".format(str(security_code)))
                # bad request
                return 'The request is invalid', 400

    except Exception as e:
        log.warning("Exception Raised: {}\n".format(e))
        return 'Internal server error', 500

    retry = 0


    if amount <= 5:

        last4_cc = str(card_num)[-4:]
        ret, output = CheapPaymentGateway(card_num,card_holder, expiry_date,security_code,amount)
        if ret:
            log.warning('Payment is processed'+'200')
            return output, 200
        else:
            return 'Internal server error: PaymentProcessor Failed', 500

    elif 20 < amount < 501:
        while retry < 2:
            ret, output = ExpensivePaymentGateway(card_num,card_holder, expiry_date,security_code,amount)
            if ret:
                log.warning('Payment is processed'+'200')
                return output, 200
            else:
                retry += 1

        log.warning("Could not process payment with ExpensivePaymentGateway")
        return 'Internal server error: PaymentProcessor Failed', 500

    else:
        while retry < 3:
            ret, output = PremiumPaymentGateway(card_num, card_holder, expiry_date, security_code, amount)
            if ret:
                log.warning('Payment is processed'+ '200')
                return output, 200
            else:
                retry += 1
        log.warning("Could not process payment with PremiumPaymentGateway")
        return 'Internal server error: PaymentProcessor Failed', 500



def CheapPaymentGateway(CreditCardNumber, CardHolder, ExpirationDate, SecurityCode, Amount):

    last4_cc = str(CreditCardNumber)[-4:]
    output = "\nProcessed Payment of € {:,.2f} for {} with CheapPaymentGateway, Card ending in {}\n".format(Amount, CardHolder, last4_cc)
    log.warning(output)
    return (1, output)

def ExpensivePaymentGateway(CreditCardNumber, CardHolder, ExpirationDate, SecurityCode, Amount):

    last4_cc = str(CreditCardNumber)[-4:]
    output = "\nProcessed Payment of € {:,.2f} for {} with ExpensivePaymentGateway, Card ending in {}\n".format(Amount, CardHolder, last4_cc)
    log.warning(output)
    return (1, output)

def PremiumPaymentGateway(CreditCardNumber, CardHolder, ExpirationDate, SecurityCode, Amount):

    last4_cc = str(CreditCardNumber)[-4:]
    output = "\nProcessed Payment of € {:,.2f} for {} with PremiumPaymentGateway, Card ending in {}\n".format(Amount, CardHolder, last4_cc)
    log.warning(output)
    return (1, output)





def sentmsg(email,msgSubj,msg):
    
    log.warning('<----------Inside message API--------->')
    try:
        
        msgObj = Mail()
        cur_date = datetime.datetime.now()
        log.warning('Inside try')
        tx_id = uuid.uuid4()
        
        url = 'https://d6hv1f8eaf.execute-api.us-east-1.amazonaws.com/scp-project/sendmail'
        sendmail = 'vikrantsonawane2@gmail.com'
        fromName = 'Hotel message'
        subject = msgSubj
        msg = msg
        receiver = "sanketsultan1997@gmail.com" #email
        
        
        params = {
        "from-email": sendmail,
        "from-name": fromName,
        "subject": subject,
        "text-part": msg,
        "recipients": [
                    {
                        "Email": receiver
                    }
                    ]
                }
        
        log.warning('URL------------>'+url)
        plainRequest = json.dumps(params)
        log.warning('Request------------>'+plainRequest)
        headers =  {"Content-Type":"application/json"}
        
        msgObj.url = url
        msgObj.request = plainRequest
        msgObj.transactionDate = cur_date
        msgObj.uuid = tx_id
        
        try:
            response =  rq.post(url,plainRequest,headers=headers)
            
            log.warning('Response Code----------->'+str(response.status_code))
            msgObj.responsecode = str(response.status_code)
            
            if response.status_code == 200:
                    data = response.json()
                    log.warning('Response---------->'+str(data))
                    msgObj.response = str(data)
                    msgObj.save()
                    return True
            # Process the data returned by the API
            else:
            # Handle the API error
                    log.warning('<-------API ERROR------>'+str(response.json()))
                    msgObj.save()
                    return False


        except Exception as e:
            log.warning('Error----------->',e)
            msgObj.save()
            return False
    except Exception as ex:
        print('Error------>'+ex)
        return False