import pytest

from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError



def test_should_register_cliente(db, client):
    # GIVEN
    data = {
        'nome': 'teste',
        'cpf': '000.000.000-00',
        'email': 'teste@teste.com',
        'telefone': '48987654321'
    }

    # WHEN

    response = client.post('/api/clientes/', data)

    # THEN
    assert response.status_code == 201


def test_should_register_transacao(client, test_cliente, test_transacao):

    # GIVEN
    data = {
        'cliente': test_cliente.cpf,
        'data_hora': test_transacao.data_hora,
        'valor': test_transacao.valor,
        'descricao': test_transacao.descricao,
        'categoria': test_transacao.categoria
    }
    
    response = client.post('/api/transacoes/', data)
    
    assert response.status_code == 201


def test_shouldnt_delete_cliente(test_cliente, test_transacao):
    test_transacao.cliente = test_cliente
    test_transacao.save()

    with pytest.raises(ProtectedError):
        test_cliente.delete()



def test_relatorio_geral_view(client, test_cliente, test_transacao):
    cliente1 = test_cliente
    cliente2 = test_cliente

    test_transacao1 = test_transacao
    test_transacao1.cliente = cliente1

    test_transacao2 = test_transacao
    test_transacao2.cliente = cliente1

    test_transacao3 = test_transacao
    test_transacao3.cliente = cliente2

    response = client.get('/api/relatorio-geral/')

    assert response.status_code == 200

    data = response.json()

    assert 'resumo_cliente' in data
    assert len(data['resumo_cliente']) == 2