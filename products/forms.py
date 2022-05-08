from django.forms import ModelForm

from products.models import Home


class HomeForm(ModelForm):
    
    class Meta:
        model = Home
        exclude = ('user', 'album', 'date_added', 'last_updated', 'home_id')