import pytest

from factory import django
from gestor_transacoes.models import Cliente, Transacao


class ClienteFactory(django.DjangoModelFactory):
    class Meta:
        model = Cliente


class TransacaoFactory(django.DjangoModelFactory):
    class Meta:
        model = Transacao


@pytest.fixture()
def test_cliente(db):
    cliente = ClienteFactory.create(
        nome='Fixture Teste',
        cpf='123.456.789-12',
        email='fixture@teste.com',
        telefone='48987654321'
    )
    return cliente


@pytest.fixture()
def test_transacao(db, test_cliente):
    transacao = TransacaoFactory.create(
        cliente=test_cliente,
        data_hora='2024-12-11 21:35',
        valor='123.45',
        descricao='Teste descricao',
        categoria='alimentacao'
    )
    return transacao
