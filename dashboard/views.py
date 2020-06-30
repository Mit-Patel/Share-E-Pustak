from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *
from authenticate_app.forms import UserForm

# Create your views here.
@login_required(login_url="/auth/login")
def index(request):
    if request.user.is_authenticated:
        book =  Book.objects.filter(user=request.user)

        # temporary code to updTE STOCKS 
        # all_books = Book.objects.all()
        # for book in all_books:
        #     update_stock(book.isbn)
        # return render(request, 'store/contact_us.html')

        return render(request, 'dashboard/index.html', {"books":book})
    else:
        return render(request,'store/index.html')

def book_detail(request, isbn):
   
    book = Book.objects.filter(isbn=isbn).first()   
    if book is not None:        
        return render(request, 'store/details.html', {"book":book})
    else:
        return redirect('404')

def display_404(request):
    return render(request,"store/404.html")

def add_user_to_book(request, id):
    bookobj = Book.objects.get(pk=id)
    bookobj.user = request.user
    bookobj.save(update_fields=['user'])    

def update_stock(id):
    is_stock_added = Book.objects.values_list('is_stock_added', flat=True).get(isbn=id,is_stock_added=False)
    if is_stock_added is not True:
        stock_count = Stock.objects.get_or_create(isbn=id)
        stock_count[0].in_stock += 1
        stock_count[0].is_out_of_stock = False
        stock_count[0].save()
    is_stock_added = Book.objects.get(isbn=id,is_stock_added=False)
    is_stock_added.is_stock_added = True 
    is_stock_added.save()

def degrade_stock(id, isbn):
    is_stock_added = Book.objects.get(pk=id)
    if is_stock_added is not False:
        stock_count = Stock.objects.get_or_create(isbn=isbn)
        stock_count[0].in_stock -= 1
        stock_count[0].is_out_of_stock = True if stock_count[0].in_stock <= 0 else False
        stock_count[0].save()
    is_stock_added = Book.objects.get(pk=id)
    is_stock_added.is_available =  False if stock_count[0].in_stock <= 0 else True
    is_stock_added.save()


@login_required(login_url="/auth/login")
def add_book(request):
    args = {}
    if request.method == "POST":
        book_form = BookForm(request.POST)
        # user = User.objects.get(username=request.user.username)
        # print(user)
        if book_form.is_valid() :
            # book_form.save(commit=False)
            # book_form.user = user
            book = book_form.save()
            # print(book_form.user)
            add_user_to_book(request, book.id)
            update_stock(book.isbn)
            args["book_form"] = book_form
            args["success"] = "Book added successfully!"
            return render(request, 'dashboard/add_book.html', args)
        else:
            args["errors"] =   str(book_form.errors)
            print(args["errors"])
            #book_form = BookForm()

            args["book_form"] = book_form
            return render(request, 'dashboard/add_book.html', args)
    else:
        book_form = BookForm()        

        args = {}
        args["book_form"] = book_form
        # args["book_upload_form"] = book_upload_form
        # args["author_form"] = author_form
        # args["pub_form"] = pub_form
        # args["cat_form"] = cat_form
        # args["author_book_form"] = author_book_form

        return render(request, 'dashboard/add_book.html', args)