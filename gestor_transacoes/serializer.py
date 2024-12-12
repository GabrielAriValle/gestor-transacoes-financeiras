from rest_framework import serializers
from rest_framework.fields import CharField
from gestor_transacoes.models import Cliente, Transacao


class ErrorSerializer(serializers.Serializer):
    mensagem = CharField()


class TransacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transacao
        read_only_fields = []
        exclude = ['id']


class ClienteSerializer(serializers.ModelSerializer):
    transacoes = TransacaoSerializer(read_only=True, many=True)

    class Meta:
        model = Cliente
        read_only_fields = []
        exclude = ['id']


class GraficoLinhasSerializer(serializers.Serializer):
    cpf = serializers.CharField(required=True, max_length=14)
    data_inicio = serializers.DateField(required=False)
    data_fim = serializers.DateField(required=False)