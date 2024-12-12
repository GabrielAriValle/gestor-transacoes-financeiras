from rest_framework.test import APITestCase

# Create your tests here.


def test_should_register_cliente(cliente):
    # GIVEN
    data = {
        'nome': 'teste',
        'cpf': '000000000000',
        'email': 'teste@teste.com',
        'telefone': '48987654321'
    }
    
    # WHEN
    response = cliente.post('/clientes', data)
    
    # THEN
    assert response.status == 200


def test_should_register_transacao(transacao):
    # GIVEN
    data = {
        ''
    }
    
    
class TestsCLientTransaction(APITestCase):
    def setUp(self):
        url_base = '/clients'
        
        return super().setUp()
    
    def test_should_register_client(self, client):
        # GIVEN
        data = {'cpf': '00000000a000'}
        
        # WHEN
        response = client.post(self.url_base, data)
        
        # THEN
        assert response.status == 200