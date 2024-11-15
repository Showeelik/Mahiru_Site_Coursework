from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.cache import cache


from .models import Recipient
from .forms import RecipientForm

class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = 'recipients/list.html'
    context_object_name = 'recipients'

    def get_queryset(self):
        if self.request.user.has_perm('recipients.view_all_recipients'):
            recipient = cache.get('recipients_{}'.format(self.request.user.id))
            if recipient is None:
                recipient = Recipient.objects.all()
                cache.set('recipients_{}'.format(self.request.user.id), recipient, 60 * 15)
        else:
            recipient = cache.get('recipients_{}'.format(self.request.user.id))
            if recipient is None:
                recipient = Recipient.objects.filter(owner=self.request.user)
                cache.set('recipients_{}'.format(self.request.user.id), recipient, 60 * 15)
        return recipient


class RecipientCreateView(LoginRequiredMixin, CreateView):
    form_class = RecipientForm
    template_name = 'recipients/form.html'
    
    success_url = reverse_lazy('recipients')
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    
class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'recipients/form.html'
    success_url = reverse_lazy('recipients')

    def form_valid(self, form):
        return super().form_valid(form)


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    success_url = reverse_lazy('recipients')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Получатель успешно удалён!")
        return super().delete(request, *args, **kwargs)
