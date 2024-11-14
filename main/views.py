from django.views.generic import TemplateView
from django.http import HttpResponse
import random

from mailing.models import Mailing
from recipients.models import Recipient
from django.core.cache import cache

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'main/home.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_authenticated:
            # Отфильтровываем рассылки по пользователю
            user_mailings = Mailing.objects.filter(owner=user)
            
            # Общее количество рассылок пользователя
            context['total_mailings'] = user_mailings.count()
            
            # Количество активных рассылок пользователя
            context['active_mailings'] = user_mailings.filter(status='STARTED').count()
            
            # Количество уникальных получателей для всех рассылок пользователя
            # Предполагается, что recipients — это ManyToMany поле в модели Mailing
            unique_recipients = Recipient.objects.filter(mailings__owner=user).distinct().count()
            context['unique_recipients'] = unique_recipients
        
        return context
    
class ContactsPageView(TemplateView):
    template_name = 'main/contacts.html'