from django.views.generic import TemplateView
from django.http import HttpResponse
import random

from mailing.models import Mailing
from recipients.models import Subscriber
from django.core.cache import cache

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'main/home.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mailings'] = Mailing.objects.count()
        context['active_mailings'] = Mailing.objects.filter(status='started').count()
        context['unique_recipients'] = Subscriber.objects.count()
        return context