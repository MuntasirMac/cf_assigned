
from django.contrib import admin
from django.urls import  path, include



v1_api_patterns=[
    path('countries/', include('country.urls')),
    
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('v1/', include(v1_api_patterns))
    ]))
]