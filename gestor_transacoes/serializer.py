from rest_framework import serializers
from rest_framework.fields import CharField
from gestor_transacoes.models import Cliente, Transacao
from datetime import datetime


class ErrorSerializer(serializers.Serializer):
    mensagem = CharField()


class TransacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transacao
        read_only_fields = []
        exclude = ['id']

    def validar_data_hora(self, value):
        if value > datetime.now():
            raise serializers.ValidationError("A data e hora não podem ser no futuro.")
        return value        


class ClienteSerializer(serializers.ModelSerializer):
    transacoes = TransacaoSerializer(read_only=True, many=True)

    class Meta:
        model = Cliente
        read_only_fields = []
        exclude = ['id']

    def validate_cpf(self, value):
        Cliente().validar_formato_cpf(value)
        return value


class GraficoLinhasSerializer(serializers.Serializer):
    cpf = serializers.CharField(required=True, max_length=14)
    data_inicio = serializers.DateField(required=False)
    data_fim = serializers.DateField(required=False)