from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import MessageForm
from .models import Message


# Create your views here.
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "messages/list.html"
    context_object_name = "messagess"

    def get_queryset(self):
        cache_key = f"messages_{self.request.user.id}"

        # Check for the correct permission
        if self.request.user.has_perm("messages.view_all_messages"):
            cache_key = "messages_all"

        messages = cache.get(cache_key)

        if messages is None:
            if self.request.user.has_perm("messages.view_all_messages"):
                messages = Message.objects.all().order_by("-id")
            else:
                messages = Message.objects.filter(owner=self.request.user).order_by("-id")

            cache.set(cache_key, messages, 60 * 15)  # Cache for 15 minutes

        return messages


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "messages/form.html"
    success_url = reverse_lazy("messages")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        cache.delete(f"messages_{self.request.user.id}")
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "messages/form.html"
    success_url = reverse_lazy("messages")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("messages")
