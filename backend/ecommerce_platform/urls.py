from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('api/accounts/', include('apps.accounts.urls')),
    path('', include('apps.catalog.urls')),
    path('api/catalog/', include('apps.catalog.urls')),
    path('orders/', include('apps.orders.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('payments/', include('apps.payments.urls')),
    path('api/payments/', include('apps.payments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
