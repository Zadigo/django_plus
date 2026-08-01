from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'


@require_GET
def legal_view(request):
    return HttpResponse(render(request, 'home.html'))
