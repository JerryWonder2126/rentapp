from pyexpat import model
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator

from accounts.forms import PublicCustomUserChangeForm
from pages.decorator import is_group, is_verified
from products.forms import HomeForm
from products.models import ImageAlbum, Home

# Create your views here.


class HomeView(TemplateView):

    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



class Dashboard(View):

    MAX_NUMBER_OF_IMAGES = 6
    MIN_NUMBER_OF_IMAGES = 4

    @method_decorator(login_required)
    @method_decorator(is_verified)
    @method_decorator(is_group(['User']))
    def get(self, request):
        return render(request, 'pages/dashboard.html')
    

    @method_decorator(login_required)
    @method_decorator(is_verified)
    @method_decorator(is_group(['User']))
    def post(self, request):
        context = {
            "show_form": True
        }
        homeForm = HomeForm()
        # print(request.POST)
        if request.POST:
            
            homeForm = HomeForm(request.POST, request.FILES)
            images_length = len(request.FILES)
            image_error = None
            if not self.MIN_NUMBER_OF_IMAGES <= images_length <= self.MAX_NUMBER_OF_IMAGES:
                image_error = "Number of images must be at least four" 
            if homeForm.is_valid() and not image_error:
                print(homeForm.cleaned_data)
                try:
                    album = self.create_image_album(request.FILES)
                    homeForm.save(request.user, album)
                    
                except Exception as e:
                    print(e)
                return redirect(to='user_homes_list')
        context['home_form'] = homeForm
        context['image_error'] = image_error
        return render(request, 'pages/dashboard.html', context)

    def create_image_album(self, images):
        album = ImageAlbum()
        album.save(images)
        return album


class UserHomeList(ListView):
    model = Home
    template_name = 'pages/list-home-for-review-user.html'


class AdminHomeList(ListView):
    template_name = 'pages/list-home-admin.html'
    # context_object_name = 'home_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = self.kwargs['status']
        context[status] = True
        print(context)
        return context
    
    def get_queryset(self):
        status = self.kwargs['status']
        print(status)
        if status not in Home.STATUS_TAGS.keys():
            raise Http404()
        return Home.objects.filter(status=status)

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
@is_verified
@is_group(['Staff'])
def listHomesForReview(request, group):
    context = {}
    if group == 'fresh':
        page_title = 'Not Reviewed'
    elif group == 'started':
        page_title = 'On Review'
    elif group == 'updated':
        page_title = 'Updated for review'
    elif group == 'on_site':
        page_title = 'On-site Review'
        context['on_site'] = True
    context['page_title'] = page_title
    return render(request, 'pages/list-home-for-review.html', context)


@login_required
@is_verified
@is_group(['Staff'])
def listHomesPassedReview(request):
    return render(request, 'pages/passed-review.html', {'resp': 'Hello'})


@login_required
@is_verified
@is_group(['Staff'])
def listHomesOnSale(request):
    return render(request, 'pages/on-sale.html', {'resp': 'Hello'})


@login_required
@is_verified
@is_group(['User'])
def listHomesUser(request):
    return render(request, 'pages/list-home-for-review-user.html', {'resp': 'Hello'})


@login_required
@is_verified
@is_group(['Staff'])
def listHomesTransactionOngoing(request):
    return render(request, 'pages/transaction-ongoing.html', {'resp': 'Hello'})


@login_required
@is_verified
@is_group(['Staff'])
def listHomesSold(request):
    return render(request, 'pages/sold.html', {'resp': 'Hello'})


@login_required
@is_verified
@is_group(['User'])
def userConfirmHome(request, confirm_type):
    context = {}

    if confirm_type == 'on_sale':
        context['on_sale_ready'] = True
    elif confirm_type == 'on_site':
        context['on_site_ready'] = True
    
    return render(request, 'pages/user-confirm-home.html', context)


@login_required
@is_verified
@is_group(['Staff'])
def reviewHomeStaff(request, unique_id='2'):
    context = {
        'price': '$34,000',
        'address': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Provident voluptatibus vel voluptatum.'
    }
    return render(request, 'pages/review-home-staff.html', context)

@login_required
@is_verified
@is_group(['User'])
def reviewHomeUser(request, unique_id='2'):
    context = {
        'priceMessage': '',
        'sellingPointsMessage': 'foolish thing',
        'imagesMessage': 'Images are not clear',
        'locationMessage': 'Where is this place? It is unrecognizable',
        'descriptionMessage': '',
        'addressMessage': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Provident voluptatibus vel voluptatum.'
    }
    return render(request, 'pages/review-home-user.html', context)


@login_required
@is_verified
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
@is_verified
@is_group('Staff')
def mark_as_staff(request):
    if request.POST:
        email = request.POST['email']
        user = get_user_model().objects.get(email=email)
        user.mark_as_staff()
    return redirect(to="index")
