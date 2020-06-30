from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from django.http import HttpResponse
from sep.settings import MEDIA_URL
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.views import View
from .models import *
from dashboard.models import *
from authenticate_app.tokens import account_activation_token
from sep import settings
from dashboard import views
# Create your views here
def index(request):
    books = Book.objects.all()
    categories = Category.objects.all()
    context = {
        "books":books,
        "categories":categories,
    }

    if request.user.is_authenticated:
        pass
    else:
        pass
    return render(request,'store/index.html',context)

@login_required(login_url="/auth/login")
def user_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':     
            print(request.POST) 
            user_form = UserForm(data=request.POST, instance=request.user)      
            user = UserProfileInfo.objects.get(user=request.user)
            print(user)
            form = UserProfileInfoForm(data=request.POST, instance=request.user)
            print(form)
            type_form = None
            if user:
                if user.type == '1': # Student
                    type_form = StudentForm(data=request.POST,instance=request.user)
                elif user.type == '2': # Faculty
                    type_form = FacultyForm(data=request.POST,instance=request.user)
                else: # Alumni
                    type_form = AlumniForm(data=request.POST,instance=request.user)
            print(type_form)           
            if user_form.is_valid() and form.is_valid() and type_form.is_valid():
                u = user_form.save()            
                t = form.save(False)                
                form.user = u
                form.save()
                custom_form = type_form.save(commit=False)
                #print(custom_form)

                type_form.user = u
                type_form.save()
                args = {}
                args['user_form'] = user_form
                args['form'] = form
                args['type_form'] = type_form
                args['success'] = "Profile updated successfully!"
                
                return render(request, 'store/my_profile.html', args)
            else:
                return render(request, 'store/my_profile.html', {"error":str(form.errors) + " " + str(type_form.errors)})
        else:
            user_form = UserForm(instance=request.user)
            print(request.user)
            user = UserProfileInfo.objects.get(user=request.user)
            print(user)
            form = UserProfileInfoForm(instance=user)
            print(form)
            type_form = None
            if user:
                if user.type == '1': # Student
                    user = Student.objects.get(user=request.user)
                    type_form = StudentForm(instance=user)
                elif user.type == '2': # Faculty
                    user = Faculty.objects.get(user=request.user)
                    type_form = FacultyForm(instance=user)
                else: # Alumni
                    user = Alumni.objects.get(user=request.user)
                    type_form = AlumniForm(instance=user)
            print(type_form)
            args = {}
            args['user_form'] = user_form
            args['form'] = form
            args['type_form'] = type_form
            
            return render(request, 'store/my_profile.html', args)
    else:
        return redirect('authenticate_app:user_login')

def about_us(request):
    return render(request,'store/about_us.html')

def contact_us(request):
    return render(request,'store/contact_us.html')

@login_required(login_url="/auth/login")
def send_request(request, book):

    current_site = get_current_site(request)
    mail_subject = 'Share-E-Pustak: A Request for your Book'
    message = render_to_string('store/book_request_link.html', {
        'book': book,
        'request_user': request.user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(book.user.pk)),
        'token':account_activation_token.make_token(book.user),
    })           
    to_email = book.user.email
    email = EmailMessage(mail_subject, message,settings.EMAIL_HOST_USER, to=[to_email])
    email.send()
    
def request_accepted(request, uidb64, token, book):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        views.degrade_stock(book.id, book.isbn)
        # current_site = get_current_site(request)
        # mail_subject = 'Share-E-Pustak: Your request has been accepted'
        # message = "Hi, you request for the book " + book.title + " has been accepted."   
        # to_email = book.user.email
        # email = EmailMessage(mail_subject, message,settings.EMAIL_HOST_USER, to=[to_email])
        # email.send()
        return HttpResponse('Thank you! The donee is now notified.')
    else:
        return HttpResponse('Link is invalid!')
    