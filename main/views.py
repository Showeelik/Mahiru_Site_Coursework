from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView
from django.http import HttpResponse
import random

# from mailing.services import MailingService
# from mailing.models import Mailing
from django.core.cache import cache

# Create your views here.

class HomeView(ListView):
    model = Mailing
    template_name = "main/home.html"
    context_object_name = "mailings"
    paginate_by = 4  # Показывать 4 продуктов на странице

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """
        Возвращает URL для редиректа.

        Args:
            request (HttpRequest):

        Returns:
            HttpResponse:
        """
        # Получаем или генерируем seed в сессии
        if "random_seed" not in self.request.session:
            self.request.session["random_seed"] = random.randint(1, 1000000)

        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> list[Mailing]:
        """
        Возвращает список продуктов.

        Returns:
            list[Mailing]:
        """
        seed = self.request.session["random_seed"]
        Mailings = cache.get(f"Mailings_{seed}")

        if Mailings is None:
            Mailings = MailingService.get_published_Mailings()
            cache.set(f"Mailings_{seed}", Mailings, 60 * 15)

        return Mailings