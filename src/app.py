# src/app.py
from flask import Flask, jsonify, request

app = Flask(__name__)

# [SIMULAÇÃO DE DADOS] Lista global para armazenar tarefas
tasks = [
    {"id": 1, "title": "Criar Diagrama de Casos de Uso", "done": True, "priority": "Alta"},
    {"id": 2, "title": "Implementar Testes Unitários", "done": False, "priority": "Média"},
]
next_id = 3

# Rota READ (Listar todas as tarefas)
@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Retorna o JSON com a lista de tarefas
    return jsonify({'tasks': tasks})

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
        # Prioridade (default: Baixa, parte da Mudança de Escopo)
        'priority': request.json.get('priority', 'Baixa') 
    }
    tasks.append(new_task)
    next_id += 1
    return jsonify({'task': new_task}), 201

# Rota UPDATE (Atualizar tarefa existente)
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    # Encontra a tarefa pelo ID
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Tarefa não encontrada.'}), 404

    # Atualiza apenas os campos que vieram no body da requisição
    if 'title' in request.json:
        task['title'] = request.json['title']
    if 'done' in request.json:
        task['done'] = request.json['done']
    if 'priority' in request.json:
        task['priority'] = request.json['priority'] # Permite atualizar a prioridade

    return jsonify({'task': task})

# Rota DELETE (Deletar tarefa)
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    initial_len = len(tasks)
    tasks = [task for task in tasks if task['id'] != task_id]

    if len(tasks) == initial_len:
        return jsonify({'error': 'Tarefa não encontrada.'}), 404
    
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