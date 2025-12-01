from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'payments', views.PaymentViewSet, basename='payment')

urlpatterns = [
    path('create/<int:order_id>/', views.create_payment, name='payment_create'),
    path('success/<int:payment_id>/', views.payment_success, name='payment_success'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('api/', include(router.urls)),
]
