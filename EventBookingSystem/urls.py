"""EventBookingSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from EBS2021.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index ,name="index"),
    path('Login', Login ,name="Login"),
    path('about', about ,name="about"),
    path('contact', contact ,name="contact"),
    path('innerhome', innerhome ,name="innerhome"),
    path('Logout', Logout ,name="Logout"),
    path('usersignup', usersignup ,name="usersignup"),
    path('Userlogin', Userlogin ,name="Userlogin"),
    path('userhome', userhome ,name="userhome"),
    path('add_event', add_event ,name="add_event"),
    path('view_event', view_event ,name="view_event"),
    path('delete_event(?p<int:pid>)', delete_event ,name="delete_event"),
    path('add_sponsor', add_sponsor,name="add_sponsor"),
    path('view_sponsor', view_sponsor ,name="view_sponsor"),
    path('delete_sponsor(?p<int:pid>)', delete_sponsor ,name="delete_sponsor"),
    path('add_category', add_category,name="add_category"),
    path('view_category', view_category ,name="view_category"),
    path('delete_category(?p<int:pid>)', delete_category ,name="delete_category"),
    path('view_user', view_user ,name="view_user"),
    path('delete_user(?p<int:pid>)', delete_user ,name="delete_user"),
    path('view_eventuser', view_eventuser ,name="view_eventuser"),
    path('view_details(?p<int:pid>)', view_details ,name="view_details"),
    path('book_now/<int:pid>', book_now ,name="book_now"),
    path('view_mybooking', view_mybooking ,name="view_mybooking"),
    path('delete_booking(?p<int:pid>)', delete_booking ,name="delete_booking"),
    path('change_passworduser', change_passworduser ,name="change_passworduser"),
    path('change_passwordadmin', change_passwordadmin ,name="change_passwordadmin"),
    path('booking_request', booking_request ,name="booking_request"),
    path('bookingdetail_user/<int:pid>',bookingdetail_user,name="bookingdetail_user"),
    path('bookingdetail_admin/<int:pid>',bookingdetail_admin,name="bookingdetail_admin"),
    path('accepted_booking',accepted_booking ,name="accepted_booking"),
    path('rejected_booking',rejected_booking ,name="rejected_booking"),
    path('all_booking',all_booking ,name="all_booking"),
    path('confirmed_booking',confirmed_booking ,name="confirmed_booking"),
    path('edit_event/<int:pid>',edit_event,name="edit_event"),
    path('edit_sponsor/<int:pid>',edit_sponsor,name="edit_sponsor"),
    path('edit_category/<int:pid>',edit_category,name="edit_category"),
    path('payment/<int:pid>',payment,name="payment"),
  #  path('v1/paymentapi',paymentApi,name="payment_api"),
    path('api/',include('api.urls')),
    ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
