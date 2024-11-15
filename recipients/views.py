from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import RecipientForm
from .models import Recipient


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = "recipients/list.html"
    context_object_name = "recipients"

    def get_queryset(self):
        cache_key = f"recipients_{self.request.user.id}"

        # Check for the correct permission
        if self.request.user.has_perm("recipients.view_all_recipients"):
            cache_key = "recipients_all"

        recipients = cache.get(cache_key)

        if recipients is None:
            if self.request.user.has_perm("recipients.view_all_recipients"):
                recipients = Recipient.objects.all().order_by("-id")
            else:
                recipients = Recipient.objects.filter(owner=self.request.user).order_by("-id")

            cache.set(cache_key, recipients, 60 * 15)  # Cache for 15 minutes

        return recipients

class RecipientCreateView(LoginRequiredMixin, CreateView):
    form_class = RecipientForm
    template_name = "recipients/form.html"

    success_url = reverse_lazy("recipients")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        cache.delete(f"recipients_{self.request.user.id}")
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "recipients/form.html"
    success_url = reverse_lazy("recipients")

    def form_valid(self, form):
        return super().form_valid(form)


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    success_url = reverse_lazy("recipients")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Получатель успешно удалён!")
        return super().delete(request, *args, **kwargs)
