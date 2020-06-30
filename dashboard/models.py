from django.db import models
from authenticate_app.models import User

BOOK_FORMAT = (
    ("1","Hard-cover"),
    ("2","Paperback"),
    ("3","Printed Copy"),
)

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=100)
    title = models.CharField(max_length=2000)
    edition = models.CharField(max_length=50)
    description = models.TextField(max_length=5000)
    publisher = models.CharField(max_length=200)
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='books/',blank=True, null=True)
    upload_date = models.DateField()
    is_available = models.BooleanField()
    book_format = models.CharField(choices=BOOK_FORMAT, max_length=50)
    language = models.CharField(max_length=100)
    is_stock_added = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.isbn
    
    
class Stock(models.Model):
    isbn = models.CharField(max_length=100)
    in_stock = models.IntegerField(default=0)
    is_out_of_stock = models.BooleanField(default=False,blank=True, null=True)

    def __str__(self):
        return self.isbn + " : " + str(self.in_stock)
    
