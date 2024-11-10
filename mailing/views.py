from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Mailing, MailingAttempt


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        return Mailing.objects.all()
    

class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing/detail.html'

class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Mailing
    fields = ['message', 'recipients', 'start_time', 'end_time']
    template_name = 'mailing/create.html'
    success_url = reverse_lazy('mailing:list')
    permission_required = 'mailing.add_mailing'

    def has_permission(self):
        return super().has_permission() or self.request.user.is_superuser
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    

class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    fields = ['message', 'recipients', 'start_time', 'end_time']
    template_name = 'mailing/update.html'
    success_url = reverse_lazy('mailing:list')
    permission_required = 'mailing.change_mailing'
    
    def has_permission(self):
        return super().has_permission() or self.request.user.is_superuser

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)
    
class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailing/delete.html'
    success_url = reverse_lazy('mailing:list')
    permission_required = 'mailing.delete_mailing'
    
    def has_permission(self):
        return super().has_permission() or self.request.user.is_superuser

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)
    

