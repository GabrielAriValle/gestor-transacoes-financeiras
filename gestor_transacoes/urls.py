from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, TransacaoViewSet, RelatoriGeralView

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='clientes')
router.register(r'transacoes', TransacaoViewSet, basename='transacoes')


urlpatterns = [
    path('', include(router.urls)),
    path('relatorio-geral/', RelatoriGeralView.as_view(), name='relatorio-geral')
]
