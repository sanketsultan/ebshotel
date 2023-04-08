from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
import logging as log
from datetime import date
import uuid

from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import datetime
from django.http import JsonResponse

from decimal import Decimal
from decimal import getcontext
import re

# Create your views here.


@api_view(['POST'])
def paymentApi(request):
    
    print('Inside API')
        # e=request.POST['email']
        # p=request.POST['pwd']
        # user=authenticate(username=e,password=p)
    if request.method == 'POST':

        try:
            
            username=request.data['email']
            password=request.data['pwd']
            user=authenticate(username=username,password=password)
            
            if user:        
                userinfo = UserPayment()
                card_num = request.data['CARD_NUMBER']
                card_holder = request.data['CARD_HOLDER']
                cardDate = request.data['END_DATE']
                security_code = request.data['CVV']
                amount = request.data['AMT']
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
                    return  Response({'RESPONSE_MSG': respMsg,'RESPONSE_CODE':respCode,'DATE_TIME':str(cur_date),'TRANSACTION_ID': str(tx_id)})
                except Exception as ex:
                    log.warning('Error--------------->',ex)
                    return  Response({'RESPONSE_MSG': 'Internal Error','RESPONSE_CODE':500,'DATE_TIME':str(cur_date)})
                    
            else:
                log.warning('INVALID USER',)
                cur_date = datetime.datetime.now()
                respMsg = 'Invalid User'
                return  Response({'RESPONSE_MSG': respMsg,'RESPONSE_CODE':400,'DATE_TIME':str(cur_date)})
            
        
        except Exception as e:
            log.warning('Error------------->',e)
            cur_date = datetime.datetime.now()
            respMsg = 'The request is invalid'
            return  Response({'RESPONSE_MSG': respMsg,'RESPONSE_CODE':400,'DATE_TIME':str(cur_date)})
            
    cur_date = datetime.datetime.now()
    respMsg = 'The request is invalid'
    return  Response({'RESPONSE_MSG': respMsg,'RESPONSE_CODE':400,'DATE_TIME':str(cur_date)})
        




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



