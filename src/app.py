# src/app.py
from flask import Flask, jsonify, request

app = Flask(__name__)

# Lista global para simular o banco de dados das tarefas
tasks = [
    {"id": 1, "title": "Criar Diagrama de Casos de Uso", "done": True, "priority": "Alta"},
    {"id": 2, "title": "Implementar Testes Unitários", "done": False, "priority": "Média"},
]
next_id = 3

# Constante Global para Otimização (perf: Commit #11)
# O dicionário de ordem de prioridade é criado apenas uma vez.
PRIORITY_ORDER = {"Alta": 3, "Média": 2, "Baixa": 1}


# FUNÇÕES AUXILIARES
def find_task(task_id):
    """Encontra uma tarefa na lista global pelo ID."""
    return next((t for t in tasks if t['id'] == task_id), None)

def validate_priority(priority):
    """Verifica se a string de prioridade é válida (fix: Commit #6)."""
    valid_priorities = ["Alta", "Média", "Baixa"] 
    if priority in valid_priorities:
        return priority
    return None


# ROTAS DA API

# Rota READ (Listar todas as tarefas)
@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Ordena a lista de tarefas usando a constante global
    sorted_tasks = sorted(
        tasks, 
        key=lambda t: (PRIORITY_ORDER.get(t['priority'], 0), t['id']), 
        reverse=True
    )
    return jsonify({'tasks': sorted_tasks})

# Rota CREATE (Criar nova tarefa)
@app.route('/tasks', methods=['POST'])
def create_task():
    global next_id
    
    # Validação de Título obrigatório
    if not request.json or 'title' not in request.json:
        return jsonify({'error': 'Título da tarefa é obrigatório.'}), 400

    # Validação de Prioridade
    priority_input = request.json.get('priority', 'Baixa')
    validated_priority = validate_priority(priority_input)
    if not validated_priority:
        return jsonify({'error': f'Prioridade inválida. Use Alta, Média ou Baixa.'}), 400


    new_task = {
        'id': next_id,
        'title': request.json['title'],
        'done': request.json.get('done', False),
        'priority': validated_priority 
    }
    tasks.append(new_task)
    next_id += 1
    return jsonify({'task': new_task}), 201

# Rota UPDATE (Atualizar tarefa existente)
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = find_task(task_id)
    
    if task is None:
        return jsonify({'error': 'Tarefa não encontrada.'}), 404

    if 'title' in request.json:
        task['title'] = request.json['title']
    if 'done' in request.json:
        task['done'] = request.json['done']
        
    # Validação de Prioridade
    if 'priority' in request.json:
        priority_input = request.json['priority']
        validated_priority = validate_priority(priority_input)
        if not validated_priority:
            return jsonify({'error': f'Prioridade inválida. Use Alta, Média ou Baixa.'}), 400
        
        task['priority'] = validated_priority

    return jsonify({'task': task})

# Rota DELETE (Deletar tarefa)
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    
    if find_task(task_id) is None:
        return jsonify({'error': 'Tarefa não encontrada.'}), 404
        
    initial_len = len(tasks)
    # Filtra a lista, removendo o item
    tasks = [task for task in tasks if task['id'] != task_id]

    if len(tasks) == initial_len:
        return jsonify({'error': 'Erro ao deletar tarefa.'}), 500
    
    return jsonify({'result': True}), 200

# Rota da Nova Feature (Filtro por Prioridade - Mudança de Escopo)
@app.route('/tasks/filter/priority/<string:task_priority>', methods=['GET'])
def filter_tasks_by_priority(task_priority):
    priority_search = task_priority.capitalize()
    
    filtered_tasks = [task for task in tasks if task['priority'] == priority_search]
    
    if not filtered_tasks:
        return jsonify({'message': f'Nenhuma tarefa com prioridade {priority_search} encontrada.'}), 404

    return jsonify({'tasks': filtered_tasks})


if __name__ == '__main__':
    app.run(debug=True)
# Fim da Aplicação