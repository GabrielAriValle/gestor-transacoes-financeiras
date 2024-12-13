from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cliente, Transacao
from .serializer import ClienteSerializer, TransacaoSerializer, GraficoLinhasSerializer
from django.db.models import Sum, F, Q, functions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class TransacaoViewSet(viewsets.ModelViewSet):
    queryset = Transacao.objects.all()
    serializer_class = TransacaoSerializer


class RelatorioGeralView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'cpf', openapi.IN_QUERY, description="CPF do cliente",
                type=openapi.TYPE_STRING, required=False,
                enum=[cliente.cpf for cliente in Cliente.objects.all()]),
        ]
    )
    def get(self, request, *args, **kwargs):
        cpf_cliente = request.query_params.get('cpf', None)

        if cpf_cliente:
            try:
                cliente = Cliente.objects.get(cpf=cpf_cliente)
            except Cliente.DoesNotExist:
                return Response({'erro': 'Cliente com este CPF nao existe'}, status=status.HTTP_404_NOT_FOUND)

            resumo_cliente = Cliente.objects.filter(cpf=cpf_cliente).annotate(
                receitas=Sum('transacao__valor', filter=Q(transacao__valor__gt=0)),
                despesas=Sum('transacao__valor', filter=Q(transacao__valor__lt=0)),
            ).annotate(
                saldo=F('receitas') + F('despesas')
            ).values('nome', 'cpf', 'receitas', 'despesas', 'saldo')

            categorias = Transacao.objects.filter(cliente=cliente).values('categoria').annotate(
                total_receitas=Sum('valor', filter=Q(valor__gt=0)),
                total_despesas=Sum('valor', filter=Q(valor__lt=0)),
                saldo_categoria=Sum('valor'),
            ).order_by('categoria')

            dados_cliente = list(resumo_cliente)
            dados_categorias = list(categorias)

            return Response({
                'resumo_cliente': dados_cliente,
                'resumo_categoria': dados_categorias
            })
        else:
            return Response({'erro': 'CPF do cliente é necessário'}, status=status.HTTP_400_BAD_REQUEST)


class GraficoLinhasView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'cpf', openapi.IN_QUERY, description="CPF do cliente",
                type=openapi.TYPE_STRING, required=False,
                enum=[cliente.cpf for cliente in Cliente.objects.all()]),
            openapi.Parameter(
                'data_inicio', openapi.IN_QUERY, description="Data de início para o filtro (YYYY-MM-DD)",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, required=False,),
            openapi.Parameter(
                'data_fim', openapi.IN_QUERY, description="Data de fim para o filtro (YYYY-MM-DD)",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, required=False),
            openapi.Parameter(
                'agrupamento', openapi.IN_QUERY, description="Agrupamento por dia ou mês",
                type=openapi.TYPE_STRING, required=False, enum=['dia', 'mes'], default='dia')
        ]
    )
    def get(self, request):
        serializer = GraficoLinhasSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        filtros = serializer.validated_data

        if 'cpf' in filtros and filtros['cpf']:
            try:
                cliente = Cliente.objects.get(cpf=filtros['cpf'])
                transacoes = Transacao.objects.filter(cliente=cliente)
            except Cliente.DoesNotExist:
                return Response({'erro': 'Cliente com este CPF nao existe'}, status=status.HTTP_404_NOT_FOUND)
        else:
            transacoes = Transacao.objects.all()

        if 'data_inicio' in filtros:
            transacoes = transacoes.filter(data_hora__date__gte=filtros['data_inicio'])
        if 'data_fim' in filtros:
            transacoes = transacoes.filter(data_hora__date__lte=filtros['data_fim'])

        agrupamento = filtros.get('agrupamento', 'dia')
        if agrupamento == 'dia':
            agrupamento_data = functions.TruncDay('data_hora')
        elif agrupamento == 'mes':
            agrupamento_data = functions.TruncMonth('data_hora')

        agrupamento_dia = transacoes.annotate(
            data=agrupamento_data
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
