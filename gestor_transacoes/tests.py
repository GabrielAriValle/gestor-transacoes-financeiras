import pytest

from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from .conftest import TransacaoFactory



def test_should_register_cliente(db, client):
    data = {
        'nome': 'teste',
        'cpf': '000.000.000-00',
        'email': 'teste@teste.com',
        'telefone': '48987654321'
    }

    response = client.post('/api/clientes/', data)

    assert response.status_code == 201


def test_shouldnt_delete_cliente(test_cliente, test_transacao):
    test_transacao.cliente = test_cliente
    test_transacao.save()

    with pytest.raises(ProtectedError):
        test_cliente.delete()


def test_shouldnt_register_cliente_cpf_invalido(db, client):
    data = {
        'nome': 'teste',
        'cpf': '00000000000',
        'email': 'teste@teste.com',
        'telefone': '48987654321'
    }

    response = client.post('/api/clientes/', data)

    assert response.status_code == 400
    assert response.json()['cpf'] == ["CPF deve estar no formato XXX.XXX.XXX-XX."]


def test_should_register_transacao(client, test_cliente, test_transacao):
    data = {
        'cliente': test_cliente.cpf,
        'data_hora': test_transacao.data_hora,
        'valor': test_transacao.valor,
        'descricao': test_transacao.descricao,
        'categoria': test_transacao.categoria
    }
    
    response = client.post('/api/transacoes/', data)
    
    assert response.status_code == 201


def test_shouldnt_register_transacao_zerada(client, test_cliente, test_transacao):
    data = {
        'cliente': test_cliente.cpf,
        'data_hora': test_transacao.data_hora,
        'valor': '0',
        'descricao': test_transacao.descricao,
        'categoria': test_transacao.categoria
    }

    response = client.post('/api/transacoes/', data)

    assert response.status_code == 400
    assert response.json()['valor'] == ["Valor deve ser diferente de zero"]


def test_relatorio_geral_view(client, test_cliente, test_transacao):
    test_transacao.cliente = test_cliente
    test_transacao.save()

    TransacaoFactory.create(
        cliente=test_cliente,
        data_hora = test_transacao.data_hora,
        valor=-200.0,
        descricao="Nova Receita Teste",
        categoria="lazer"
    )

    response = client.get('/api/relatorio-geral/')

    assert response.status_code == 200

    data = response.json()

    assert 'resumo_cliente' in data and len(data['resumo_cliente']) == 1

    cliente_data = next(item for item in data['resumo_cliente'] if item['cpf'] == '123.456.789-12')
    assert cliente_data['receitas'] == 123.45 and cliente_data['despesas'] == -200.0 and cliente_data['saldo'] == -76.55

    assert 'resumo_categoria' in data and len(data['resumo_categoria']) == 2

    categorias = data['resumo_categoria']
    assert any(categoria['categoria'] == 'alimentacao' and categoria['total_receitas'] == 123.45 for categoria in categorias)
    assert any(categoria['categoria'] == 'lazer' and categoria['total_despesas'] == -200.0 for categoria in categorias)


# TO DO
def test_grafico_linhas_view(client, test_cliente, test_transacao):
    test_transacao.cliente = test_cliente
    test_transacao.save()
    
    params = {
        'cpf': test_cliente.cpf,
        'data_inicio': '2015-03-14',
        'data_fim': '2022-04-12'
    }
    response = client.get('/api/grafico-linhas/', params)

    assert response.status_code == 200


def test_grafico_linhas_cliente_inexistente(client):
    params = {'cpf': '000.000.000-00'}

    response = client.get('/api/grafico-linhas/', params)

    assert response.status_code == 404 and response.json()['erro'] == 'Cliente com este CPF nao existe'
