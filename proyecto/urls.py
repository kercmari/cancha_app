"""
URL configuration for proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include,re_path
from Reserva import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('getInfoCanchaById/<int:id_cancha>',views.get_info_cancha_by_id,name='getInfoCanchaById'),
    path('getPersonaById/<int:id_persona>',views.get_persona_by_id,name='getPersonaById'),
    path('reservar/<int:id_horario>',views.reservarCancha,name='reservar'),
    path('canchas/',views.getListadoCanchas,name='getListadoCanchas'),
    path('registro/',views.registro_request,name='registro'),
    path('login/',views.login_request,name='login'),
    path('logout/',views.logout_request,name='logout'),
    # path("", views.MainView.as_view(), name='landing'),
    path('api/', include('Reserva.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

urlpatterns += [re_path(r'^.*$', TemplateView.as_view(template_name='index.html'), name='home')]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)