# import django libs
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.views import View

# import python libs
import urllib.request
import urllib.parse
import random
import json

# import classes
from .forms import UserForm, UserProfileInfoForm, LoginForm
from .models import User, UserProfileInfo
from .tokens import account_activation_token
from sep import settings


# user registration view
def register(request):
    registered = False
    
    # return HttpResponse("Reg")
    if request.method == "POST":
        # get data from POST request
        print(request.POST)
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        
        # validate data 
        if user_form.is_valid() and profile_form.is_valid() :
            # save the user
            user = user_form.save()

            #set the password
            user.set_password(user.password)
            user.save()

            # save the profile info without commit
            profile = profile_form.save(commit=False)
            profile.user = user

            # save the profile picture in to the dir
            # if 'profile_pic' in request.FILES:
            #     profile.profile_pic = request.FILES['profile_pic']
            
            profile.mobile_verified = True
            profile.user.is_active = False
            profile.save()

            current_site = get_current_site(request)
            mail_subject = 'Share-E-Pustak: Activate your account'
            message = render_to_string('authenticate_app/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })           
            to_email = user.email
            email = EmailMessage(mail_subject, message,settings.EMAIL_HOST_USER, to=[to_email])
            email.send()

            registered = True
            return JsonResponse({
                "status":"success",
                "message":"Registered Successfully!"
            })            
        else:
            # send error message
            return JsonResponse({
                "status":"error",
                "message": str(user_form.errors) + " \n " + str(profile_form.errors)
            })
            # return HttpResponse("error")
            # return render(request,'authenticate_app/register.html', {"user_error":user_form.errors, "profile_error":profile_form.errors})
            # print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # render the registration form
    return render(request, 'authenticate_app/register.html', {'user_form':user_form, 'profile_form': profile_form, 'registered':registered })

# send and verify OTP views
def send_otp(request):   
    if request.method == "POST":
        # generate an 6 digit otp
        otp = random.randint(100000,999999)
        # set the required data (apikey, number of client, message and ame of sender)
        data =  urllib.parse.urlencode({
            'apikey': '7f2Mflp3ZOI-6bMfp5DiPu5Mynq4wE4mFo578gXCKk', 
            'numbers': '+91'+request.POST['mobile_no'],
            'message' : 'OTP: ' + str(otp) , 
            'sender': 'TXTLCL',
            'test':'true'
        })

        # encode the data
        data = data.encode('utf-8')        
        
        print(otp)
        
        # store the otp in session
        request.session['otp'] = str(otp)
        
        # send the sms 
        request_otp = urllib.request.Request("https://api.textlocal.in/send/?")
        # print(request_otp)
        
        # get the response back
        response = urllib.request.urlopen(request_otp, data)
        response_json = response.read().decode('utf-8')
        response_data = json.loads(response_json)
        # print(response_data['status'])
        
        return JsonResponse(data={"success":"true"})
    else:
        return render(request,"authenticate_app/404.html")

# verify the otp
def verify_otp(request):
    if request.method == "POST":
        # check the session otp and otp user entered
        if request.POST['otp'] == request.session['otp']:
            # send json back to ajax
            print("success")
            return JsonResponse({
                "status":"success",
                "message":"OTP Verified"
            })
            # return HttpResponse("success")
        else:
            print("error")
            # send error message
            return JsonResponse({
                "status":"error",
                "message":"OTP Verification Failed!"
            })
            # return render(request,'authenticate_app/register.html', {"error":"OTP Verification Failed!"})
            # return HttpResponse("error")
    else:
        # render 404 page
        return render(request,"authenticate_app/404.html")

# check if the username already exists
def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)

# login view
def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('index')
            else:
                login_form = LoginForm()

                return render(request,'authenticate_app/login.html', {"errors":"Account is not active! Please activate your account!","login_form":login_form})
        else:
            login_form = LoginForm()

            return render(request,'authenticate_app/login.html', {"errors":"Invalid username or password!","login_form":login_form})
            
    else:
        login_form = LoginForm()
        return render(request, 'authenticate_app/login.html',{"login_form":login_form})

# logout view
@login_required(login_url="/auth/login")
def user_logout(request):
    logout(request)
    return redirect('index')

# activate account after email activation link has been clicked
class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            profile = UserProfileInfo.objects.get(user=user)
            profile.email_verified = True
            profile.mobile_no_verified = True
            profile.save()
            
            #login(request, user)
            # return redirect('home')
            return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')