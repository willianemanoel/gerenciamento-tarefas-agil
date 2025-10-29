# src/app.py
from flask import Flask, jsonify, request

app = Flask(__name__)

# [SIMULAÇÃO DE DADOS] Lista global para armazenar tarefas
tasks = [
    {"id": 1, "title": "Criar Diagrama de Casos de Uso", "done": True, "priority": "Alta"},
    {"id": 2, "title": "Implementar Testes Unitários", "done": False, "priority": "Média"},
]
next_id = 3

# ===================================================================
# FUNÇÃO AUXILIAR REFATORADA PARA O COMMIT #5
# A busca por tarefa estava repetida em PUT e DELETE.
# ===================================================================
def find_task(task_id):
    """Encontra uma tarefa na lista global pelo ID."""
    return next((t for t in tasks if t['id'] == task_id), None)
# ===================================================================

# Rota READ (Listar todas as tarefas)
@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Define a ordem de prioridade (Alta > Média > Baixa)
    priority_order = {"Alta": 3, "Média": 2, "Baixa": 1}

    # Ordena a lista de tarefas: 
    sorted_tasks = sorted(
        tasks, 
        key=lambda t: (priority_order.get(t['priority'], 0), t['id']), 
        reverse=True
    )
    
    # Retorna o JSON com a lista de tarefas ordenadas por prioridade
    return jsonify({'tasks': sorted_tasks})

# Rota CREATE (Criar nova tarefa)
@app.route('/tasks', methods=['POST'])
def create_task():
    global next_id
    
    # Validação de dados (Essencial para testes)
    if not request.json or 'title' not in request.json:
        return jsonify({'error': 'Título da tarefa é obrigatório.'}), 400

    new_task = {
        'id': next_id,
        'title': request.json['title'],
        'done': request.json.get('done', False),
        'priority': request.json.get('priority', 'Baixa') 
    }
    tasks.append(new_task)
    next_id += 1
    return jsonify({'task': new_task}), 201

# Rota UPDATE (Atualizar tarefa existente)
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    # CHAMA A FUNÇÃO AUXILIAR REFATORADA
    task = find_task(task_id)
    
    if task is None:
        return jsonify({'error': 'Tarefa não encontrada.'}), 404

    # Atualiza apenas os campos que vieram no body da requisição
    if 'title' in request.json:
        task['title'] = request.json['title']
    if 'done' in request.json:
        task['done'] = request.json['done']
    if 'priority' in request.json:
        task['priority'] = request.json['priority']

    return jsonify({'task': task})

# Rota DELETE (Deletar tarefa)
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    
    # Verifica se a tarefa existe antes de tentar deletar
    if find_task(task_id) is None:
        return jsonify({'error': 'Tarefa não encontrada.'}), 404
        
    initial_len = len(tasks)
    # Filtra a lista, removendo o item
    tasks = [task for task in tasks if task['id'] != task_id]

    # Esta verificação é redundante após o find_task, mas mantida para segurança
    if len(tasks) == initial_len:
         # Se a tarefa já foi encontrada (acima), esta linha nunca deve ser alcançada, mas é um bom fallback
        return jsonify({'error': 'Erro ao deletar tarefa.'}), 500
    
    return jsonify({'result': True}), 200

# Rota da Nova Feature (Filtro por Prioridade - Mudança de Escopo)
@app.route('/tasks/filter/priority/<string:task_priority>', methods=['GET'])
def filter_tasks_by_priority(task_priority):
    # Converte a prioridade para o formato correto ('Alta', 'Média', 'Baixa')
    priority_search = task_priority.capitalize()
    
    filtered_tasks = [task for task in tasks if task['priority'] == priority_search]
    
    if not filtered_tasks:
        return jsonify({'message': f'Nenhuma tarefa com prioridade {priority_search} encontrada.'}), 404

    return jsonify({'tasks': filtered_tasks})


if __name__ == '__main__':
    # Roda a aplicação em modo debug
    app.run(debug=True)