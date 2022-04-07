from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class HomeView(TemplateView):

    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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
