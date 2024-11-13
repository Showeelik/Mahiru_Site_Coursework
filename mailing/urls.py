from django.urls import path

from .views import (MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView)



urlpatterns = [
    path("", view=MailingListView.as_view(), name="mailings_list"),
]
