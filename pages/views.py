import re
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator

from accounts.forms import PublicCustomUserChangeForm
from pages.decorator import is_group
from pages.helpers import create_album
from products.forms import HomeForm, HomeAuditForm
from products.models import Home, HomeAuditMessage


# Create your views here.


class HomeView(TemplateView):

    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



class Dashboard(View):

    MAX_NUMBER_OF_IMAGES = 6
    MIN_NUMBER_OF_IMAGES = 4

    @method_decorator([login_required, is_group(['User'])])
    def get(self, request):
        user_homes = Home.objects.filter(user=request.user)
        homes_not_sold = user_homes.exclude(status=Home.Status.SOLD).count()
        homes_sold = user_homes.filter(status=Home.Status.SOLD).count()

        context = {
            'homes_sold': homes_sold,
            'homes_not_sold': homes_not_sold
        }

        print(context)

        return render(request, 'pages/dashboard.html', context)
    

    @method_decorator([login_required, is_group(['User'])])
    def post(self, request):
        context = {
            "show_form": True   # This makes the form visible on page
        }
            
        homeForm = HomeForm(request.POST)
        images_length = len(request.FILES)
        image_error = None
        if not self.MIN_NUMBER_OF_IMAGES <= images_length <= self.MAX_NUMBER_OF_IMAGES:
            image_error = "Number of images must be at least four" 
        if homeForm.is_valid() and not image_error:
            album = create_album(request.FILES)
            homeForm.save(request.user, album)
            return redirect(to='user_homes_list')
        context['home_form'] = homeForm
        context['image_error'] = image_error
        return render(request, 'pages/dashboard.html', context)


@method_decorator([login_required, is_group(['User'])], name='dispatch')
class UserHomeList(ListView):
    model = Home
    template_name = 'pages/list-home-for-review-user.html'

    def get_queryset(self):
        homes = super().get_queryset().filter(user=self.request.user)
        for  home in homes:
            home.reviewing = True if home.status == 'remote_review' else False
            home.review_updated = True if home.status in ['updated_for_review', 'not_reviewed'] else False
            home.on_site = True if home.status == 'onsite_review' else False
            home.passed_review = True if home.status == 'passed_review' else False
        return homes


@method_decorator([login_required, is_group(['Staff'])], name='dispatch')
class AdminHomeList(ListView):
    template_name = 'pages/list-home-admin.html'
    # context_object_name = 'home_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = self.kwargs['status']
        context[status] = True
        return context
    
    def get_queryset(self):
        status = self.kwargs['status']
        if status not in Home.STATUS_TAGS.keys():
            raise Http404()
        return Home.objects.filter(status=status)


class AuditHomeAdmin(View):

    @method_decorator([login_required, is_group(['Staff'])])
    def get(self, request, unique_home_hash):
        home = get_object_or_404(Home, home_id=unique_home_hash)
        homeAudit = HomeAuditMessage.objects.get(home=home)
        form = HomeAuditForm(instance=homeAudit)
        context = {
            'form': form,
            'home': home,
            'prefill': form.initial
        }
        return render(request, 'pages/review-home-staff.html', context)

    @method_decorator([login_required, is_group(['Staff'])])
    def post(self, request, unique_home_hash):
        home = get_object_or_404(Home, home_id=unique_home_hash)
        homeAudit = HomeAuditMessage.objects.get(home=home)
        form = HomeAuditForm(request.POST, instance=homeAudit)
        if form.is_valid():
            form.save(home=home)
            return redirect('review_list', status='remote_review')
        context = {
            'form': form,
            'home': home,
            'prefill': form.data
        }
        return render(request, 'pages/review-home-staff.html', context)


class AuditHomeUser(View):

    @method_decorator([login_required, is_group(['User'])])
    def get(self, request, unique_home_hash):
        home = get_object_or_404(Home, home_id=unique_home_hash, user=request.user)
        homeAudit = HomeAuditMessage.objects.get(home=home)
        form = HomeForm(instance=home)
        context = {
            'home_form': form,
            'audit': homeAudit,
            'prefill': form.initial
        }
        return render(request, 'pages/review-home-user.html', context)

    @method_decorator([login_required, is_group(['User'])])
    def post(self, request, unique_home_hash):
        home = get_object_or_404(Home, home_id=unique_home_hash, user=request.user)
        homeAudit = HomeAuditMessage.objects.get(home=home)
        form = HomeForm(request.POST, instance=home)
        images_length = len(request.FILES)
        image_error = None
        if homeAudit.album_msg:
            if not self.MIN_NUMBER_OF_IMAGES <= images_length <= self.MAX_NUMBER_OF_IMAGES:
                image_error = "Number of images must be at least four" 
        if form.is_valid() and not image_error:
            album = create_album(request.FILES, home.album.album_hash) if homeAudit.album_msg else None
            home = form.save(request.user, album, False)
            home.mark_as_updated_review()   # This saves the user and changes it's status
            return redirect(to='user_homes_list')
        context = {
            'home_form': form,
            'audit': homeAudit,
            'prefill': form.data
        }
        context['image_error'] = image_error
        return render(request, 'pages/review-home-user.html', context)
    
    
class ConfirmHomeOnSale(View):

    @method_decorator([login_required, is_group(['User'])])
    def get(self, request, home_unique_hash):
        home = get_object_or_404(Home, home_id=home_unique_hash, user=request.user)
        
        context = {
            'on_sale_ready': True,
            'home': home
        }

        return render(request, 'pages/user-confirm-home.html', context)
    
    @method_decorator([login_required, is_group(['User'])])
    def post(self, request, home_unique_hash):
        response = {'ok': True}
        try:
            home = get_object_or_404(Home, home_id=home_unique_hash, user=request.user)
            home.to_on_sale()
        except Exception as e:
            response['ok'] = False
        return JsonResponse(response)


class UserConfirmHomeOnSite(View):

    @method_decorator([login_required, is_group(['User'])])
    def get(self, request, home_unique_hash):
        home = get_object_or_404(Home, home_id=home_unique_hash, user=request.user)
        
        context = {
            'on_site_ready': True,
            'home': home
        }

        return render(request, 'pages/user-confirm-home.html', context)


@login_required
@is_group(['Staff'])
def takeActionOnHome(request, action, unique_home_hash):
    if action not in ['pass_review', 'breakdown_review', 'pass_remote_review', 'to_onsale', 'ongoing', 'complete']:
        raise Http404()
    home = get_object_or_404(Home, home_id=unique_home_hash)
    if action == 'pass_review':
        home.pass_review()
    elif action == 'breakdown_review':
        home.breakdown_review()
    elif action == 'pass_remote_review':
        home.pass_remote_review()
        return redirect('review_list', status='onsite_review')
    elif action == 'to_onsale':
        home.to_on_sale()
    elif action == 'ongoing':
        home.mark_as_ongoing()
    elif action == 'complete':
        home.mark_as_sold()
    return redirect(request.META['HTTP_REFERER'])


def faqs(request):
    return render(request, 'pages/faqs.html')


def products_page(request, group=''):
    context = {}
    if not group:
        context['all_products'] = True
    else:
        context['group'] = group
    return render(request, 'pages/products.html', context)


def house_page(request, group, identifier):
    return render(request, 'pages/single-house.html', {'resp': 'Hello'})


def offers(request, group, filterby, filter):
    context = {}
    if filterby == 'type':
        context['byType'] = True
    elif filterby == 'region':
        context['byRegion'] = True
    context['group'] = group
    context['filter'] = filter
    return render(request, 'pages/list-offers.html', context)


@login_required

@is_group(['User'])
def userConfirmHome(request):
    context = {
        'on_site_ready': True
    }
    
    return render(request, 'pages/user-confirm-home.html', context)


class UserConfirmHomeOnSite(TemplateView):
    template_name = 'pages/user-confirm-home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['on_site_ready'] = True
        return context


@login_required

@is_group(['User', 'Staff'])
def profile(request, unique_id='2'):

    user_form = PublicCustomUserChangeForm(instance=request.user)

    if request.POST:
        request.POST['is_staff'] = True
        user_form = PublicCustomUserChangeForm(request.POST, instance=request.user)
        if user_form.is_valid():
            print(user_form.cleaned_data['first_name'])
            # user_form.save()
    
    context = {
        'form': user_form
    }

    return render(request, 'pages/profile.html', context)


@login_required

@is_group('Staff')
def mark_as_staff(request):
    if request.POST:
        email = request.POST['email']
        user = get_user_model().objects.get(email=email)
        user.mark_as_staff()
    return redirect(to="index")
