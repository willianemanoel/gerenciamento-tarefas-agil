# tests/test_tasks.py
import pytest
from src.app import app

# Fixture para configurar o cliente de teste do Flask
@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Cria um cliente de teste para simular requisições HTTP
    with app.test_client() as client:
        yield client

# TESTE 1: CREATE (Criação com Sucesso, incluindo a nova Prioridade)
def test_create_task_success(client):
    response = client.post(
        '/tasks',
        json={'title': 'Nova Tarefa de Teste', 'priority': 'Alta'},
        content_type='application/json'
    )
    # Verifica o código 201 (Created)
    assert response.status_code == 201
    data = response.get_json()
    assert data['task']['title'] == 'Nova Tarefa de Teste'
    assert data['task']['priority'] == 'Alta'

# TESTE 2: VALIDAÇÃO DE ENTRADA (Obrigatório para o requisito de testes)
def test_create_task_invalid_input(client):
    """Verifica se o sistema retorna erro 400 se o campo 'title' estiver faltando."""
    response = client.post(
        '/tasks',
        json={'done': False}, # Falta o 'title'
        content_type='application/json'
    )
    # Verifica o código 400 (Bad Request)
    assert response.status_code == 400
    data = response.get_json()
    assert 'obrigatório' in data['error']

# TESTE 3: UPDATE (Atualização de uma tarefa)
def test_update_task_status(client):
    """Verifica a atualização do campo 'done'."""
    response = client.put(
        '/tasks/1',
        json={'done': False}, # Tarefa 1 é True inicialmente
        content_type='application/json'
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['task']['done'] == False

# TESTE 4: NOVO RECURSO (Filtro por Prioridade - Teste da Mudança de Escopo)
def test_filter_tasks_by_priority_success(client):
    """Verifica se o endpoint de filtro está funcionando corretamente."""
    # Filtrar por 'Alta'
    response = client.get('/tasks/filter/priority/alta')
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['tasks']) == 1 # Apenas a tarefa 1 deve ser encontrada
    assert data['tasks'][0]['priority'] == 'Alta'