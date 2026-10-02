# API de Lista de Tarefas (To-Do)

API REST desenvolvida como atividade acadêmica para praticar CRUD, métodos HTTP, validação de dados e filtros com Query Parameters usando FastAPI.

- **Professor:** Jonathas Jivago
- **Aluno:** F. Mailson da Silva Sousa
- **Disciplina:** Programação para Internet II
- **Atividade 02:** Desenvolvimento de uma API de Lista de Tarefas

O [guia da atividade](guia.md) contém a transcrição dos requisitos do PDF fornecido pelo professor.

## Tecnologias

- Python 3.12 ou superior (o projeto utiliza 3.12 em `.python-version`).
- FastAPI para criação das rotas e documentação automática.
- Pydantic para validação dos dados.
- uv para gerenciamento do ambiente e das dependências.

## Como executar

Com Git e uv instalados, clone o projeto e entre na pasta:

```powershell
git clone https://github.com/MailsonSousa88/todolist-api.git
cd todolist-api
```

Instale as dependências definidas no projeto:

```powershell
uv sync
```

Inicie o servidor de desenvolvimento:

```powershell
uv run fastapi dev main.py
```

Não é necessário ativar o ambiente virtual manualmente ao usar `uv run`.

Com o servidor em execução, acesse:

| Endereço | Finalidade |
| --- | --- |
| [API](http://127.0.0.1:8000/) | Mensagem de boas-vindas |
| [Swagger UI](http://127.0.0.1:8000/docs) | Documentação e execução de requisições com **Try it out** |
| [ReDoc](http://127.0.0.1:8000/redoc) | Consulta da documentação |

As tarefas são armazenadas em uma lista em memória. Reiniciar o servidor, inclusive pela recarga automática após alterações no código, apaga os dados cadastrados.

## Rotas

| Método | Caminho | Operação | Status de sucesso |
| --- | --- | --- | --- |
| GET | `/` | Exibir mensagem de boas-vindas | 200 |
| GET | `/tarefas` | Listar tarefas e receber filtros | 200 |
| GET | `/tarefas/{id}` | Consultar uma tarefa pelo UUID | 200 |
| POST | `/tarefas` | Criar uma tarefa | 201 |
| PUT | `/tarefas/{id}` | Atualizar uma tarefa | 200 |
| DELETE | `/tarefas/{id}` | Excluir uma tarefa, sem corpo na resposta | 204 |

Nas rotas com `{id}`, utilize o UUID retornado ao criar ou listar uma tarefa. Um UUID válido que não existe na lista gera `404`. Dados que não atendem ao schema, como um ID malformado ou um título curto demais, geram `422`.

## Criar uma tarefa

Envie um JSON para `POST /tarefas`:

```json
{
  "titulo": "Estudar FastAPI",
  "descricao": "Revisar rotas, schemas e parâmetros de consulta",
  "tags": ["python", "fastapi", "estudos"]
}
```

| Campo | Obrigatório | Regra |
| --- | --- | --- |
| `titulo` | Sim | Texto com 10 a 80 caracteres |
| `descricao` | Não | Texto ou `null`; padrão `null` |
| `tags` | Não | Lista de strings; padrão `[]` |

O servidor gera o `id` como UUID, define `concluida` como `false` e preenche `data_criacao` e `data_atualizacao` automaticamente. As datas são geradas separadamente e podem diferir em microssegundos na criação.

## Atualizar uma tarefa

Envie um JSON para `PUT /tarefas/{id}`, substituindo `{id}` pelo UUID da tarefa:

```json
{
  "titulo": "Estudar FastAPI",
  "descricao": "Revisão de rotas e schemas concluída",
  "tags": ["python", "fastapi"],
  "concluida": true
}
```

Na atualização, `titulo` e `concluida` são obrigatórios. O ID e a data de criação são preservados, e a data de atualização é renovada.

Se `descricao` ou `tags` forem omitidos, recebem os padrões `null` e `[]`; os valores anteriores desses campos não são preservados.

## Filtros de consulta

A rota `GET /tarefas` recebe os seguintes parâmetros opcionais:

| Parâmetro | Tipo | Critério |
| --- | --- | --- |
| `concluida` | Booleano | Situação igual a `true` ou `false` |
| `tag` | Texto | Tag exata presente na lista de tags, distinguindo maiúsculas e minúsculas |
| `titulo` | Texto | Trecho contido no título, ignorando maiúsculas e minúsculas |

Exemplos de URLs:

```text
/tarefas
/tarefas?concluida=true
/tarefas?concluida=false
/tarefas?tag=python
/tarefas?titulo=python
/tarefas?concluida=false&tag=python&titulo=estudar
```

Quando combinados com `&`, todos os filtros informados precisam ser atendidos. A busca por título usa `lower()` e não remove acentos nem corrige erros de digitação.

**Limitação atual:** o `return tarefas_filtradas` está dentro do `for`. Com filtros, a listagem retorna apenas a primeira tarefa correspondente; quando nenhuma corresponde, a função retorna `None`, causando erro de validação da resposta (500). O retorno precisa ficar após o laço para concluir a filtragem.

## Estrutura do projeto

| Arquivo | Responsabilidade |
| --- | --- |
| [main.py](main.py) | Aplicação FastAPI, rotas e filtros |
| [tarefa_schema.py](tarefa_schema.py) | Schemas de entrada, armazenamento e resposta |
| [repositorio_de_tarefas.py](repositorio_de_tarefas.py) | Lista de tarefas em memória |
| [pyproject.toml](pyproject.toml) | Metadados e dependências do projeto |
| [uv.lock](uv.lock) | Versões resolvidas das dependências |

## Pendências da atividade

- Corrigir o retorno da listagem com filtros.
- Implementar ordenação por campo e direção.
- Implementar paginação.
- Implementar consulta por período de criação.

Na implementação atual, a consulta por ID usa `TarefaSchema` como modelo de resposta e exibe somente `titulo`, `descricao` e `tags`. A listagem, a criação e a atualização utilizam o schema público, que também inclui ID, situação e datas.
