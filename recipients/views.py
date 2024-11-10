from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Subscriber

class SubscriberListView(ListView):
    model = Subscriber
    template_name = 'recipients/subscriber_list.html'

class SubscriberCreateView(CreateView):
    model = Subscriber
    fields = ['email', 'full_name', 'comment']
    template_name = 'recipients/subscriber_form.html'
    success_url = reverse_lazy('recipients:list')
    
class SubscriberUpdateView(UpdateView):
    model = Subscriber
    fields = ['email', 'full_name', 'comment']
    template_name = 'recipients/subscriber_form.html'
    success_url = reverse_lazy('recipients:list')
    
class SubscriberDeleteView(DeleteView):
    model = Subscriber
    template_name = 'recipients/subscriber_delete.html'
    success_url = reverse_lazy('recipients:list')
    