from django.contrib import admin
from django.utils.translation import gettext as _

from products.models import Home, HomeAuditMessage, Image, ImageAlbum


# Register your models here.
@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ['user', 'home_id', 'album', 'price', 'short_description', 'apartment_type', 'status', 'tags', 'last_updated', 'date_added']
    fieldsets = (
        (None, {"fields": ("user", "home_id")}),
        (_("Main info"), {"fields": ("short_description", "price", 'apartment_type', 'album', 'status')}),
        (
            _("Extra Info"),
            {
                "fields": (
                    "selling_point",
                    "address"
                ),
            },
        ),
    )
    # add_fieldsets = (
    #     (
    #         None,
    #         {
    #             "classes": ("wide",),
    #             "fields": ("email", "password1", "password2"),
    #         },
    #     ),
    # )
    search_fields = ("short_description", "user", "home_id", "apartment_type")
    ordering = ("short_description", "last_updated", "date_added")


@admin.register(HomeAuditMessage)
class HomeAuditMessageAdmin(admin.ModelAdmin):
    model = HomeAuditMessage
    list_display = ["home", "short_description_msg", "price_msg", 'apartment_type_msg', 'album_msg', 'selling_point_msg', 'address_msg']
    fieldsets = (
        (_("Messages"), {"fields": ("short_description_msg", "price_msg", 'apartment_type_msg', 'album_msg', 'selling_point_msg', 'address_msg')}),
    )
    # add_fieldsets = (
    #     (
    #         None,
    #         {
    #             "classes": ("wide",),
    #             "fields": ("email", "password1", "password2"),
    #         },
    #     ), 9
    # )
    search_fields = ("home", 'last_updated')
    ordering = ("last_updated",)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    model = Image
    list_display = ["album", "image"]
    fieldsets = (
        (None, {"fields": ("album", "image")}),
    )

@admin.register(ImageAlbum)
class ImageAdmin(admin.ModelAdmin):
    model = ImageAlbum
    list_display = ["album_hash"]
    # fieldsets = (
    #     (None, {"fields": ("album", "image")}),
    # )