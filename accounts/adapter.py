from allauth.account.adapter import DefaultAccountAdapter

class UserAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super(UserAccountAdapter, self).save_user(request, user, form, commit=False)
        # user.first_name = self.cleaned_data['first_name']
        # user.last_name = self.cleaned_data['last_name']
        # user.mobile_number = self.cleaned_data['mobile_number']
        # user.address = self.cleaned_data['address']
        # user.username = getUsernameFromEmail(self.cleaned_data['email'])
        return user