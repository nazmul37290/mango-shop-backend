from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductList, ProductViewSet, OrderViewSet,CustomerOrderList,
    order_summary,custom_token_view)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', ProductList.as_view(), name="ProductList"),
    path('api/token/', custom_token_view, name='token_obtain_pair'),
    path("api/order-summary/", order_summary, name='ordersummary'),
    path("api/customer-orders/", CustomerOrderList.as_view(), name="customer-orders"),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)