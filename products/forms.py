from django.forms import ModelForm

from products.models import Home, Image, ImageAlbum


class HomeForm(ModelForm):
    
    class Meta:
        model = Home
        exclude = ('user', 'album', 'date_added', 'last_updated', 'home_id', 'status', 'tags')

    
    def save(self, user, album, commit=True):
        home_obj = super(HomeForm, self).save(commit=False)
        home_obj.album = album
        home_obj.user = user
        if commit:
            home_obj.save()
        return home_obj