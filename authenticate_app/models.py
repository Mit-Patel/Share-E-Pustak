from django.db import models

# import the inbuilt User model from Authentication module
from django.contrib.auth.models import User


# User types choices
USER_TYPE_CHOICES = (
    ("1","Student"),
    ("2","Alumni"),
    ("3","Faculty"),
)

# User profile model
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    mobile_no = models.CharField(max_length=10)
    mobile_no_verified = models.BooleanField(null=True)
    email_verified = models.BooleanField(null=True)
    # profile_pic = models.ImageField(upload_to="profile_pics",blank=True)
    city = models.CharField(max_length=30)
    type = models.CharField(max_length=15,choices=USER_TYPE_CHOICES, default="1")

    def __str__(self):
        return self.user.username