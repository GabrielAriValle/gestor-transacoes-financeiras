from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cliente, Transacao
from .serializer import ClienteSerializer, TransacaoSerializer, GraficoLinhasSerializer
from django.db.models import Sum, F, Q, functions


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class TransacaoViewSet(viewsets.ModelViewSet):
    queryset = Transacao.objects.all()
    serializer_class = TransacaoSerializer


class RelatorioGeralView(APIView):
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
    

class GraficoLinhasView(APIView):
    def get(self, request):
        serializer = GraficoLinhasSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        filtros = serializer.validated_data

        try:
            cliente = Cliente.objects.get(cpf=filtros['cpf'])
        except:
            return Response({'erro': 'Cliente com este CPF nao existe'}, status=status.HTTP_404_NOT_FOUND)
        
        transacoes = Transacao.objects.filter(cliente=cliente)
        if 'data_inicio' in filtros:
            transacoes = transacoes.filter(data_hora__date__gte=filtros['data_inicio'])
        if 'data_fim' in filtros:
            transacoes = transacoes.filter(data_hora__date__lte=filtros['data_fim'])

        agrupamento_dia = transacoes.annotate(
            data=functions.TruncDay('data_hora')
        ).values('data').annotate(
            receitas=Sum('valor', filter=Q(valor__gt=0)),
            despesas=Sum('valor', filter=Q(valor__lt=0)),
        ).order_by('data')

        dados_grafico = []
        saldo_acumulado = 0
        for transacao in agrupamento_dia:
            saldo_acumulado += (transacao['receitas'] or 0) + (transacao['despesas'] or 0)
            dados_grafico.append({
                'data': transacao['data'],
                'receitas': transacao['receitas'] or 0,
                'despesas': transacao['despesas'] or 0,
                'saldo_acumulado': saldo_acumulado
            })

        return Response(dados_grafico, status=status.HTTP_200_OK)

