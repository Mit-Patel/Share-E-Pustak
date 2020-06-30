from django.db import models
# import the inbuilt User model from Authentication module


from authenticate_app.models import UserProfileInfo, User

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    branch = models.CharField(max_length=50)
    semester = models.IntegerField()
    year = models.IntegerField()
    enrollment_no = models.CharField(max_length=12)
    cpi = models.FloatField()

    def __str__(self):
        return self.user.username
    

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    branch = models.CharField(max_length=50)
    
    def __str__(self):
        return self.user.username

class Alumni(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    branch = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    post = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
   