Ótimo ponto! Vou adaptar os códigos para que tenham o estilo e a simplicidade que um estudante de Engenharia de Software aplicaria em um trabalho universitário, focando na clareza didática, nos comentários explicativos e no cumprimento dos requisitos mínimos.

Aqui estão os códigos ajustados, com foco na simplicidade e nos requisitos:

1. Arquivos na Raiz do Repositório
a) README.md (Documentação Essencial)
Mantenho o foco na estrutura exigida, incluindo a justificativa da mudança de escopo.

Markdown

# gerenciamento-tarefas-agil: Projeto Ágil de Engenharia de Software

## 1. Objetivo e Escopo
O objetivo é simular o desenvolvimento de um **Sistema de Gerenciamento de Tarefas** para uma startup de logística, utilizando metodologias ágeis. O escopo inicial é a implementação de um **CRUD (Create, Read, Update, Delete)** de tarefas via API REST com Python/Flask.

## 2. Metodologia Adotada
A metodologia utilizada é o **Kanban**, implementada no GitHub Projects. As colunas **A Fazer**, **Em Progresso** e **Concluído** permitem a visualização clara do fluxo de trabalho.

## 3. Código Base e Tecnologias
- **Linguagem:** Python
- **Framework Web:** Flask (Simplicidade e rapidez para API REST)
- **Testes:** Pytest
- **CI/CD:** GitHub Actions

## 4. Gestão de Mudanças (Alteração de Escopo)
### Mudança: Adição de Prioridade nas Tarefas

Durante o ciclo de desenvolvimento, identificamos a necessidade (simulando um requisito do cliente de logística) de **priorizar tarefas (Alta, Média, Baixa)**.

**Justificativa:** Em projetos de logística, a priorização dinâmica é vital. Esta mudança de escopo foi implementada para garantir que tarefas críticas sejam identificadas e resolvidas primeiro, aumentando a eficiência operacional.

**Ações no Projeto:**
1. Adição do campo `priority` ao modelo de dados (ver `src/app.py`).
2. Criação de uma rota de filtro (`/tasks/filter/priority/`).

## 5. Controle de Qualidade (CI com GitHub Actions)
Configuramos um pipeline de Integração Contínua (`.github/workflows/main.yml`) que executa os testes automatizados (`pytest tests/`) a cada nova alteração no código. Isso garante que a qualidade do software seja mantida e que a nova feature (Prioridade) não tenha quebrado o CRUD existente.

## 6. Como Executar (Instruções Simples)
1. Instale as dependências: `pip install -r requirements.txt`
2. Execute a API: `python src/app.py`
3. Acesse em `http://127.0.0.1:5000/`.