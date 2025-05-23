from django.urls import path
from .views import (
    country_list,
    country_detail_view,
    country_create_view,
    country_update_view,
    country_delete_view,
    same_region_countries_view,
    countries_by_language_view,
    search_country_by_name,
)


urlpatterns = [
    path('list/', country_list, name='country_list'),
    path('detail/<int:id>/', country_detail_view, name='country_detail'),
    path('create', country_create_view, name='country_create'),
    path('update/<int:id>', country_update_view, name='country_update'),
    path('delete/<int:id>', country_delete_view, name='country_delete'),
    path('same-region-countries/<int:id>', same_region_countries_view, name='same_region_countries'),
    path('countries-by-language', countries_by_language_view, name='countries_by_language'),
    path('search-country-by-name', search_country_by_name, name='search_country_by_name'),
]