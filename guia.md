# Atividade prática

Desenvolvimento de uma API de Lista de Tarefas (To-Do)

## Objetivo

Desenvolver uma API REST para gerenciamento de uma lista de tarefas (To-Do List), utilizando os conceitos estudados em aula sobre desenvolvimento de APIs, métodos HTTP, parâmetros de rota, parâmetros de consulta (Query Parameters), manipulação de dados e organização de aplicações web.

A API deverá permitir criar, consultar, atualizar e excluir tarefas, além de possibilitar pesquisas e ordenação dos resultados.

## 1. Modelo de uma tarefa

Cada tarefa deverá possuir, no mínimo, os seguintes dados:

- `id` — identificador único da tarefa;
- `titulo` — título da tarefa;
- `descricao` — descrição da tarefa;
- `concluida` — indica se a tarefa foi concluída (`true` ou `false`);
- `tags` — lista de etiquetas associadas à tarefa;
- `data_criacao` — data e hora em que a tarefa foi criada;
- `data_atualizacao` — data e hora da última atualização da tarefa.

Exemplo:

```json
{
    "id": 1,
    "titulo": "Estudar FastAPI",
    "descricao": "Revisar criação de APIs REST",
    "concluida": false,
    "tags": ["python", "fastapi", "backend"],
    "data_criacao": "2026-09-09T08:30:00",
    "data_atualizacao": "2026-09-09T08:30:00"
}
```

As datas devem ser preenchidas automaticamente pela aplicação. O usuário não deverá precisar informar `data_criacao` ao cadastrar uma tarefa.

Quando uma tarefa for alterada, `data_atualizacao` deverá ser atualizada automaticamente.

## 2. Endpoints obrigatórios

A API deverá implementar os seguintes endpoints.

### 2.1 Criar uma tarefa

```http
POST /tarefas
```

Deverá receber os dados necessários para criar uma nova tarefa.

Exemplo de requisição:

```json
{
    "titulo": "Estudar Python",
    "descricao": "Revisar funções e classes",
    "tags": ["python", "estudos"]
}
```

A aplicação deverá:

- gerar automaticamente o `id`;
- definir `concluida` como `false` inicialmente;
- registrar `data_criacao`;
- registrar `data_atualizacao`.

### 2.2 Listar todas as tarefas

```http
GET /tarefas
```

Deverá retornar todas as tarefas cadastradas.

Exemplo:

```http
GET /tarefas
```

### 2.3 Consultar uma tarefa específica

```http
GET /tarefas/{id}
```

Deverá retornar uma tarefa a partir do seu identificador.

Exemplo:

```http
GET /tarefas/5
```

Caso a tarefa não exista, a API deverá retornar uma resposta HTTP adequada, como `404 Not Found`.

### 2.4 Atualizar uma tarefa

```http
PUT /tarefas/{id}
```

Deverá permitir a atualização dos dados de uma tarefa.

Exemplo:

```http
PUT /tarefas/5
```

```json
{
    "titulo": "Estudar FastAPI",
    "descricao": "Estudar rotas, parâmetros e respostas",
    "concluida": true,
    "tags": ["python", "fastapi"]
}
```

A `data_atualizacao` deverá ser atualizada automaticamente.

### 2.5 Excluir uma tarefa

```http
DELETE /tarefas/{id}
```

Deverá excluir uma tarefa.

Exemplo:

```http
DELETE /tarefas/5
```

Caso a tarefa não exista, deverá ser retornado um erro adequado.

## 3. Consultas utilizando Query Parameters

Além do CRUD, a API deverá permitir realizar consultas utilizando Query Parameters.

### 3.1 Filtrar tarefas por situação

```http
GET /tarefas?concluida=true
```

Deverá retornar somente as tarefas concluídas.

Exemplo:

```http
GET /tarefas?concluida=false
```

Deverá retornar somente as tarefas ainda não concluídas.

### 3.2 Filtrar por tag

```http
GET /tarefas?tag=python
```

Deverá retornar as tarefas que possuem a tag informada.

Exemplo:

```http
GET /tarefas?tag=python
```

Também deverá ser possível consultar outras tags:

```http
GET /tarefas?tag=estudos
```

### 3.3 Filtrar por título

```http
GET /tarefas?titulo=python
```

Deverá retornar tarefas cujo título contenha o texto informado.

A pesquisa não precisa necessariamente considerar apenas uma correspondência exata.

Por exemplo:

```http
GET /tarefas?titulo=python
```

poderá retornar:

- Estudar Python;
- Exercícios de Python;
- Projeto final com Python.

## 4. Ordenação dos resultados

O endpoint de listagem deverá permitir definir a ordenação através de Query Parameters.

```http
GET /tarefas?ordenar_por=campo&ordem=asc|desc
```

O parâmetro `ordenar_por` deverá permitir, pelo menos, os seguintes campos:

- `id`
- `titulo`
- `data_criacao`
- `data_atualizacao`

O parâmetro `ordem` deverá aceitar:

- `asc` — ordem crescente;
- `desc` — ordem decrescente.

### Exemplos

Listar tarefas da mais antiga para a mais recente:

```http
GET /tarefas?ordenar_por=data_criacao&ordem=asc
```

Listar tarefas da mais recente para a mais antiga:

```http
GET /tarefas?ordenar_por=data_criacao&ordem=desc
```

Ordenar alfabeticamente pelo título:

```http
GET /tarefas?ordenar_por=titulo&ordem=asc
```

Ordenar pelo título em ordem decrescente:

```http
GET /tarefas?ordenar_por=titulo&ordem=desc
```

## 5. Combinação de filtros

A API deverá permitir combinar diferentes Query Parameters.

Por exemplo:

```http
GET /tarefas?concluida=false&tag=python
```

Deverá retornar somente as tarefas:

- que ainda não foram concluídas; e
- que possuem a tag `python`.

Também deverá ser possível combinar filtros e ordenação:

```http
GET /tarefas?concluida=false&tag=python&ordenar_por=data_criacao&ordem=desc
```

Nesse caso, deverão ser retornadas as tarefas pendentes que possuem a tag `python`, ordenadas da mais recente para a mais antiga.

## 6. Paginação

Implemente paginação na listagem de tarefas.

O endpoint deverá aceitar:

```http
GET /tarefas?pagina=1&limite=10
```

Onde:

- `pagina` indica a página desejada;
- `limite` indica a quantidade máxima de tarefas retornadas.

Exemplo:

```http
GET /tarefas?pagina=2&limite=10
```

Deverá retornar a segunda página, contendo até 10 tarefas.

A resposta poderá conter informações adicionais, como:

```json
{
    "pagina": 2,
    "limite": 10,
    "total": 35,
    "tarefas": []
}
```

## 7. Consulta por período

Implemente uma consulta que permita encontrar tarefas criadas dentro de determinado período.

Exemplo:

```http
GET /tarefas?data_inicio=2026-09-01&data_fim=2026-09-09
```

A API deverá retornar somente as tarefas criadas dentro do período informado.

## Entrega (pode ser em trio)

- Colocar o projeto no github.
- Apresentar a API em funcionamento;
