from rest_framework.test import APITestCase

# Create your tests here.


def test_should_register_cliente(db, client):
    # GIVEN
    data = {
        'nome': 'teste',
        'cpf': '000000000000',
        'email': 'teste@teste.com',
        'telefone': '48987654321'
    }

    # WHEN

    response = client.post('/api/clientes/', data)

    # THEN
    assert response.status_code == 201


def test_should_register_transacao(client, test_cliente):
    # GIVEN
    data = {
        'cliente': test_cliente.cpf,
        'data_hora': '24/05/24',
        'valor': '123',
        'descricao': 'Teste',
        'categoria': 'Alimentacao'
    }
    
    response = client.post('/api/transacoes/', data)
    
    assert response.status == 201