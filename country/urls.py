from django.urls import path
from .views import (
    country_list,
    country_detail_view,
    country_create_view,
)


urlpatterns = [
    path('list/', country_list, name='country_list'),
    path('detail/<int:id>/', country_detail_view, name='country_detail'),
    path('create', country_create_view, name='country_create'),
]