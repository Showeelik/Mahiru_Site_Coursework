from django.urls import path
from .views import SubscriberListView, SubscriberCreateView

urlpatterns = [
    path('', SubscriberListView.as_view(), name='subscriber_list'),
    path('add', SubscriberCreateView.as_view(), name='subscriber_add'),
    path('<int:pk>/edit', SubscriberCreateView.as_view(), name='subscriber_edit'),
    path('<int:pk>/delete', SubscriberCreateView.as_view(), name='subscriber_delete'),
]
