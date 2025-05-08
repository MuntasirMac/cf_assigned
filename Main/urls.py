
from django.contrib import admin
from django.urls import  path, include
from .views import login_view, logout_view, signup_view



v1_api_patterns=[
    path('countries/', include('country.urls')),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('signup', signup_view, name='signup'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('v1/', include(v1_api_patterns))
    ]))
]