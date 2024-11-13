from django.forms import BaseModelForm
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Message
from .forms import MessageForm

# Create your views here.
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messages/list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        if self.request.user.has_perm('messages_mailing.view_all_messages'):
            return Message.objects.all()
        return Message.objects.all()

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'messages/form.html'
    success_url = reverse_lazy('messages')

    def form_valid(self, form):
        return super().form_valid(form)

class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'messages/form.html'
    success_url = reverse_lazy('messages')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_valid(form)

class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('messages')