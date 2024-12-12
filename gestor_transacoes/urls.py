from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, TransacaoViewSet, RelatorioGeralView, GraficoLinhasView

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='clientes')
router.register(r'transacoes', TransacaoViewSet, basename='transacoes')


urlpatterns = [
    path('', include(router.urls)),
    path('relatorio-geral/', RelatorioGeralView.as_view(), name='relatorio-geral'),
    path('grafico-linhas/', GraficoLinhasView.as_view(), name='grafico-linhas')
]
