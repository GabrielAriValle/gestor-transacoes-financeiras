from rest_framework import serializers
from rest_framework.fields import CharField
from gestor_transacoes.models import Cliente, Transacao
import re


class ErrorSerializer(serializers.Serializer):
    mensagem = CharField()


class TransacaoSerializer(serializers.ModelSerializer):
    cliente = serializers.SlugRelatedField(slug_field='cpf', queryset=Cliente.objects.all())

    class Meta:
        model = Transacao
        fields = ['id', 'cliente', 'data_hora', 'valor', 'descricao', 'categoria']

    def validate_valor(self, value):
        if value == 0:
            raise serializers.ValidationError("Valor deve ser diferente de zero")
        return value


class ClienteSerializer(serializers.ModelSerializer):
    transacoes = TransacaoSerializer(read_only=True, many=True)

    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'cpf', 'email', 'telefone', 'transacoes']

    def validate_cpf(self, value):
        formato_cpf_esperado = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'
        if not re.match(formato_cpf_esperado, value):
            raise serializers.ValidationError("CPF deve estar no formato XXX.XXX.XXX-XX.")
        return value


class GraficoLinhasSerializer(serializers.Serializer):
    cpf = serializers.CharField(required=False, max_length=14)
    data_inicio = serializers.DateField(required=False)
    data_fim = serializers.DateField(required=False)
    agrupamento = serializers.ChoiceField(choices=['dia', 'mes'], required=False, default='dia')
