from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cliente, Transacao
from .serializer import ClienteSerializer, TransacaoSerializer
from django.db.models import Sum, F, Q


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class TransacaoViewSet(viewsets.ModelViewSet):
    queryset = Transacao.objects.all()
    serializer_class = TransacaoSerializer


class RelatoriGeralView(APIView):
    def get(self, request, *args, **kwargs):
        cliente = Cliente.objects.all().annotate(
            receitas=Sum('transacao__valor', filter=Q(transacao__valor__gt=0)),
            despesas=Sum('transacao__valor', filter=Q(transacao__valor__lt=0)),
        ).annotate(
            saldo = F('receitas') + F('despesas')
        ).values('nome', 'cpf', 'receitas', 'despesas', 'saldo')

        categorias = Transacao.objects.values('categoria').annotate(
            total_receitas=Sum('valor', filter=Q(valor__gt=0)),
            total_despesas=Sum('valor', filter=Q(valor__lt=0)),
            saldo_categoria=Sum('valor'), 
        ).order_by('categoria')

        dados_cliente = list(cliente)
        dados_categorias = list(categorias)

        return Response({
            'resumo_cliente': dados_cliente,
            'resumo_categoria': dados_categorias
        })
    