from django.urls import path
from .views import (
    country_list,
    country_detail_view,
    country_create_view,
    country_update_view,
    # country_delete_view,
)


urlpatterns = [
    path('list/', country_list, name='country_list'),
    path('detail/<int:id>/', country_detail_view, name='country_detail'),
    path('create', country_create_view, name='country_create'),
    path('update/<int:id>', country_update_view, name='country_update'),
    # path('delete/<int:id>/', country_delete_view, name='country_delete'),
]