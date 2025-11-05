# testes/test_tasks.py
import pytest
import json 
# Importa 'app', 'tasks' e 'next_id' para poder manipular o estado da aplicação
from src.app import app, tasks, next_id 

# ESTADO INICIAL PADRÃO (para resetar antes de cada teste)
INITIAL_TASKS = [
    {"id": 1, "title": "Criar Diagrama de Casos de Uso", "done": True, "priority": "Alta"},
    {"id": 2, "title": "Implementar Testes Unitários", "done": False, "priority": "Média"},
]
INITIAL_NEXT_ID = 3

# --- SETUP E ISOLAMENTO DE TESTES (COMMIT #7: test) ---
def setup_function():
    """Restaura o estado inicial da lista global 'tasks' antes de cada teste."""
    global next_id
    tasks.clear()
    tasks.extend(INITIAL_TASKS)
    next_id = INITIAL_NEXT_ID # Garante que o próximo ID de criação será 3

# Fixture para configurar o cliente de teste do Flask
@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Cria um cliente de teste para simular requisições HTTP
    with app.test_client() as client:
        yield client

# TESTE 1: CREATE (Criação com Sucesso, incluindo a nova Prioridade)
def test_create_task_success(client):
    """Verifica a criação de uma nova tarefa (POST) com sucesso."""
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
    # Garante que o ID foi incrementado corretamente
    assert data['task']['id'] == 3 

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
    # Graças ao setup_function, a lista está isolada e tem apenas 2 tarefas.
    response = client.get('/tasks/filter/priority/alta')
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['tasks']) == 1 # Agora isso deve passar!
    assert data['tasks'][0]['priority'] == 'Alta'

# TESTE 5: TESTE DE VALIDAÇÃO DE PRIORIDADE INVÁLIDA (Aumento de Cobertura)
def test_create_task_invalid_priority(client):
    """Verifica se a validação de prioridade na criação retorna status 400, cobrindo o FIX."""
    invalid_task_data = {
        'title': 'Tarefa Inválida',
        'priority': 'Urgente' # Valor que não é Alta, Média ou Baixa
    }
    response = client.post('/tasks',
                           data=json.dumps(invalid_task_data),
                           content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'Prioridade inválida.' in data['error']
    
# NOVO TESTE: Garantir que a lista ordenada é retornada (Implícito na Mudança de Escopo)
def test_get_tasks_is_ordered_by_priority(client):
    """Verifica se a rota GET /tasks retorna as tarefas ordenadas por prioridade (Alta > Média)."""
    # Lista inicial: ID 1 (Alta), ID 2 (Média)
    response = client.get('/tasks')
    data = response.get_json()
    assert response.status_code == 200
    assert len(data['tasks']) == 2
    assert data['tasks'][0]['priority'] == 'Alta' 
    assert data['tasks'][1]['priority'] == 'Média' 