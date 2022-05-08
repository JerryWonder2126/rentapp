from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from allauth.account.signals import email_confirmed
from allauth.account.models import EmailAddress

from accounts.managers import CustomUserManager


# Create your models here.
class CustomUser(AbstractUser):
    # add additional fields in here
    # username = models.CharField(_('username'), max_length=50, null=False)
    username = None
    first_name = models.CharField(_('first name'), max_length=50, null=False)
    last_name = models.CharField(_('last name'), max_length=50, null=False)
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    mobile_number = models.IntegerField(_('mobile number'), null=True)
    address = models.TextField(_('address'), max_length=250, null=False)
    is_verified = models.BooleanField(_('verification status'), default=False, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name}"
    
    def mark_as_staff(self):
        self.is_staff = True
        user_group_status = Group.objects.get(name='User')
        staff_group_status = Group.objects.get(name='Staff')
        self.groups.add(staff_group_status)
        self.groups.remove(user_group_status)
        self.save()        


@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    user = EmailAddress.objects.get(email=email_address).user
    user.is_verified = True
    user.save()


@receiver(post_save, sender=CustomUser)
def add_group(sender, instance, created, **kwargs):
    """
    Adds group to user model when created based on is_superuser status
    """
    user_group_status = Group.objects.get(name='User')
    staff_group_status = Group.objects.get(name='Staff')
    if created:
        if instance.is_superuser:
            instance.groups.add(staff_group_status)
        else:
            instance.groups.add(user_group_status)
        instance.save()
