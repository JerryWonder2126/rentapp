from django.forms import ModelForm

from products.models import Home, HomeAuditMessage


class HomeForm(ModelForm):
    
    class Meta:
        model = Home
        exclude = ('user', 'album', 'date_added', 'last_updated', 'home_id', 'status', 'tags')

    
    def save(self, user, album=None, commit=True):
        home_obj = super(HomeForm, self).save(commit=False)
        if album:
            home_obj.album = album
        home_obj.user = user
        if commit:
            home_obj.save()
        return home_obj

class HomeAuditForm(ModelForm):

    class Meta:
        model = HomeAuditMessage
        exclude = ('home', 'last_updated')
    
    def save(self, home, commit=True):
        auditMessage = super(HomeAuditForm, self).save(commit=False)
        auditMessage.home = home.mark_as_onremote_review()
        if commit:
            auditMessage.save()
        return auditMessage