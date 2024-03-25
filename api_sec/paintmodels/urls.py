from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, OrderViewSet, PaintViewSet, TokenVerifyView, UserProfileViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
router = DefaultRouter()
router.register(r'paints', PaintViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'userprofiles', UserProfileViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]