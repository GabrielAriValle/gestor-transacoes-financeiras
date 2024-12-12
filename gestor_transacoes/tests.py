from rest_framework.test import APITestCase

# Create your tests here.


def test_should_register_cliente(client):
    # GIVEN
    data = {
        'nome': 'teste',
        'cpf': '000000000000',
        'email': 'teste@teste.com',
        'telefone': '48987654321'
    }
    
    # WHEN
    response = client.post('/clientes', data)
    
    # THEN
    assert response.status == 200


def test_should_register_transacao(client):
    # GIVEN
    data = {
        'cliente': '12345678912'
        'data_hora': ''
        'valor': '123'
        'descricao': 'Teste'
        'categoria': 'Alimentacao'
    }
    
    response = client.post('/transacoes', data)
    
    assert response.status == 200