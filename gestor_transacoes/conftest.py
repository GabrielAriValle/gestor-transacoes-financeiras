import pytest

from factory import django
from .models import Cliente

class ClienteFactory(django.DjangoModelFactory):
    class meta:
        model = Cliente


@pytest.fixture()
def test_cliente(db):
    cliente = ClienteFactory.create(
        nome = "Fixture Teste",
        cpf = "12345678912",
        email = "fixture@teste.com",
        telefone = "48987654321"
    )
    return cliente
    
