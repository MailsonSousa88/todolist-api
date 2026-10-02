# Organização dos testes

Esta pasta contém os testes automatizados da API de gerenciamento de tarefas, organizados conforme a ordem das seções do [`GUIA_TESTES.md`](../GUIA_TESTES.md).

## Módulos de teste

| Ordem | Seção do guia | Módulo | Responsabilidade |
| ---: | --- | --- | --- |
| 1 | 3.1 — Testes de criação | [`test_criacao_tarefas.py`](test_criacao_tarefas.py) | Criação de tarefas e verificação dos dados gerados. |
| 2 | 3.2 — Testes de consulta | [`test_consulta_tarefas.py`](test_consulta_tarefas.py) | Listagem e consulta de tarefas por identificador. |
| 3 | 3.3 — Testes de atualização | [`test_atualizacao_tarefas.py`](test_atualizacao_tarefas.py) | Atualização dos dados e do estado das tarefas. |
| 4 | 3.4 — Testes de exclusão | [`test_exclusao_tarefas.py`](test_exclusao_tarefas.py) | Exclusão de tarefas e verificações posteriores. |
| 5 | 4 e 4.1 — Filtros e consultas | [`test_consulta_filtro_tarefas.py`](test_consulta_filtro_tarefas.py) | Filtros individuais e combinação de filtros. |
| 6 | 5 — Testes de ordenação | [`test_ordenacao_tarefas.py`](test_ordenacao_tarefas.py) | Ordenação por data, título e identificador. |
| 7 | 6 — Validação e tratamento de erros | [`test_validacao_tratamento_erros_tarefas.py`](test_validacao_tratamento_erros_tarefas.py) | Requisições inválidas e respostas de erro da API. |

## Arquivos de apoio

- [`conftest.py`](conftest.py): define as fixtures compartilhadas, incluindo o `TestClient`.
- [`__init__.py`](__init__.py): identifica `tests` como um pacote Python.

## Execução

Na raiz do projeto, execute:

```bash
uv run pytest -v
```
