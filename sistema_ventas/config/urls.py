from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("productos/", include("apps.productos.urls")),
    path("clientes/", include("apps.clientes.urls")),
    path("", RedirectView.as_view(url="/productos/"), name = "home"),
    path('ventas/', include('apps.ventas.urls')),
    # Aquí agregaremos las URLs de nuestras apps después
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)