# Projeto de Engenharia de Software Ágil: Gerenciamento de Tarefas

Este projeto implementa uma API simples de CRUD (Create, Read, Update, Delete) para gerenciamento de tarefas utilizando Flask, com o objetivo de demonstrar a aplicação de conceitos de Engenharia de Software Distribuída.

O desenvolvimento seguiu as diretrizes do trabalho, com foco nos seguintes requisitos:

1.  Desenvolvimento Distribuído e Semântico (Total de 10+ Commits)
2.  Controle de Integração Contínua (CI) via GitHub Actions
3.  Documentação e Análise de Requisitos (Diagramas UML)
4.  Implementação da Mudança de Escopo (Filtro por Prioridade)

---

## 1. Justificativa da Mudança de Escopo: Prioridade

O requisito de CRUD foi expandido para incluir o campo **Prioridade** (`Alta`, `Média`, `Baixa`) nas tarefas. Esta funcionalidade foi implementada para atender à necessidade de gerenciamento ágil, permitindo:

* **Ordenação:** A lista principal de tarefas é retornada sempre ordenada por prioridade (Alta primeiro).
* **Filtro:** Permite listar tarefas apenas por um nível de prioridade específico.

## 2. Configuração e Execução Local

Para rodar a aplicação em seu ambiente local:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/willianemanoel/gerenciamento-tarefas-agil](https://github.com/willianemanoel/gerenciamento-tarefas-agil)
    ```
2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Execute o servidor da API:**
    ```bash
    python src/app.py
    ```
    A API será iniciada em `http://127.0.0.1:5000/`.

## 3. Controle de Qualidade

* Os testes unitários estão implementados na pasta `testes/`.
* O pipeline de **Integração Contínua (CI)** está configurado no `.github/workflows/main.yml` para rodar os testes automaticamente em cada *push* realizado na *branch* principal (`main`).

## 4. Rotas da API (Endpoints)

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| **GET** | `/tasks` | Lista todas as tarefas, ordenadas por prioridade. |
| **GET** | `/tasks/filter/priority/<prioridade>` | Filtra tarefas pelo nível de prioridade (Ex: `/tasks/filter/priority/Media`). |
| **POST** | `/tasks` | Cria uma nova tarefa. Requer `title`. |
| **PUT** | `/tasks/<id>` | Atualiza campos de uma tarefa existente (título, status ou prioridade). |
| **DELETE** | `/tasks/<id>` | Deleta uma tarefa pelo ID. |