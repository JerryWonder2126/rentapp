from uuid import uuid4
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from products.helpers import get_upload_path

# Create your models here.


# class UserProduct (models.Model):
#     location = models.CharField(max_length=10)


class ImageAlbum(models.Model):
    album_hash = models.UUIDField(_("album hash"), default=uuid4)
    def default(self):
        return self.images.first()
    
    def save(self, album_images, *args, **kwargs):
        super(ImageAlbum, self).save(*args, **kwargs)
        for image in album_images:
            Image.objects.create(image=image, album=self)
            
        
        return self
    
    def __str__(self):
        return str(self.album_hash)


class Image(models.Model):
    image = models.ImageField(_('image'), upload_to=get_upload_path)
    album = models.ForeignKey(ImageAlbum, models.CASCADE)


class Home(models.Model):

    class ApartmentType(models.TextChoices):
        A_ROOM = _('a room')#, _('a room')
        FACE_ME = _('face me and face you')#, _('face me and face you')
        ONE_SELF_CON = _('one bedroom self con')#, _('one bedroom self con')
        TWO_SELF_CON = _('two bedroom self con')#, _('two bedroom self con')
        THREE_SELF_CON = _('three bedroom self con')#, _('three bedroom self con')
        DUPLEX = _('duplex')#, _('duplex')
        UPSTAIRS = _('upstairs')#, _('upstairs')
        BUNGALOW = _('bungalow')#, _('bungalow')
    
    class Status(models.TextChoices):
        NOT_REVIEWED = _('not_reviewed')
        REMOTE_REVIEW = _('remote_review')
        UPDATED_FOR_REVIEW = _('updated_for_review')
        ONSITE_REVIEW = _('onsite_review')
        PASSED_REVIEW = _('passed_review')
        ON_SALE = _('on_sale')
        ONGOING = _('ongoing')
        SOLD = _('sold')
    

    STATUS_TAGS = {
        Status.NOT_REVIEWED: _('not reviewed'),
        Status.REMOTE_REVIEW: _('not reviewed, on-review'),
        Status.UPDATED_FOR_REVIEW: _('not reviewed, on-review'),
        Status.ONSITE_REVIEW: _('not reviewed, on-review'),
        Status.PASSED_REVIEW: _('reviewed'),
        Status.ON_SALE: _('reviewed, on sale'),
        Status.ONGOING: _('reviewed, on sale, ongoing'),
        Status.SOLD: _('reviewed, sold')
    }

    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    album = models.OneToOneField(ImageAlbum, models.CASCADE)
    price = models.IntegerField(_('price'))
    short_description = models.CharField(_("short description"), max_length=50)
    address = models.TextField(_("address"))
    apartment_type = models.CharField(_("apartment type"), max_length=30, choices=ApartmentType.choices)
    selling_point = models.TextField(_("selling point"))
    home_id = models.UUIDField(_("home id"), default=uuid4, unique=True)
    status = models.CharField(_("status"), max_length=50, choices=Status.choices, default=Status.NOT_REVIEWED)
    tags = models.CharField(_("tags"), max_length=50, editable=False)
    date_added = models.DateField(_("date added"), auto_now_add=True)
    last_updated = models.DateField(_("last_updated"), auto_now=True)

    def __str__(self):
        return str(self.short_description)
    
    def save(self, **kwargs) -> None:
        self.set_tags()
        return super().save(**kwargs)
    
    def set_tags(self):
        self.tags = self.STATUS_TAGS[self.status]
    
    def pass_remote_review(self, commit=True):
        """ Changes home status to 'onsite_review' """
        self.status = self.Status.ONSITE_REVIEW
        self.set_tags()
        if commit:
            self.save()
        return self

    def pass_review(self, commit=True):
        """ Changes home status to 'passed_review' """
        self.status = self.Status.PASSED_REVIEW
        self.set_tags()
        if commit:
            self.save()
        return self
    
    def breakdown_review(self, commit=True):
        """ Reverts home status to 'not_reviewed' """
        self.status = self.Status.NOT_REVIEWED
        self.set_tags()
        if commit:
            self.save()
        return self
    
    def mark_as_onremote_review(self, commit=True):
        """ Changes home status to 'passed_review' """
        self.status = self.Status.REMOTE_REVIEW
        self.set_tags()
        if commit:
            self.save()
        return self
    
    def mark_as_updated_review(self, commit=True):
        """ Changes home status to 'passed_review' """
        self.status = self.Status.UPDATED_FOR_REVIEW
        self.set_tags()
        if commit:
            self.save()
        return self
    
    def to_on_sale(self, commit=True):
        """ Changes home status to 'on sale'  """
        self.status = self.Status.ON_SALE
        self.set_tags()
        if commit:
            self.save()
        return self
    
    def mark_as_ongoing(self, commit=True):
        """ Changes home status to 'ongoing', i.e negotiations has begun """
        self.status = self.Status.ONGOING
        self.set_tags()
        if commit:
            self.save()
        return self
    
    def mark_as_sold(self, commit=True):
        """ Marks home as sold """
        self.status = self.Status.SOLD
        self.set_tags()
        if commit:
            self.save()
        return self


class HomeAuditMessage(models.Model):
    home = models.OneToOneField(Home, models.CASCADE)
    price_msg = models.TextField(_("price message"), null=True, blank=True)
    album_msg = models.TextField(_("album message"), null=True, blank=True)
    short_description_msg = models.TextField(_("short description message"), null=True, blank=True)
    address_msg = models.TextField(_("address message") , null=True, blank=True)
    apartment_type_msg = models.TextField(_("aparment type message"), null=True, blank=True)
    selling_point_msg = models.TextField(_("selling point message"), null=True, blank=True)
    last_updated = models.DateField(_("last_updated"), auto_now=True)

    def __str__(self):
        return f"{self.home.short_description} audit message"


@receiver(post_save, sender=Home)
def initiate_audit_message_for_home(sender, instance, created, **kwargs):
    if created:
        audit_message = HomeAuditMessage(home=instance)
        audit_message.save()
