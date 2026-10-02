import pytest
from fastapi.testclient import TestClient

from repositorio_de_tarefas import listaDeTarefas
from src.main import app


@pytest.fixture(autouse=True)
def limpar_repositorio():
    listaDeTarefas.clear()

    yield

    listaDeTarefas.clear()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def dados_tarefa():
    return {
        "titulo": "Estudar programação para internet II",
        "descricao": "Revisar e praticar os ensinamentos sobre programação para internet II",
        "tags": ["python", "fastapi"],
    }


@pytest.fixture
def dados_tarefa_tags():
    return {
        "titulo": "Estudar programação para internet II",
        "descricao": "Revisar e praticar os ensinamentos sobre programação para internet II",
        "tags": [
            "python",
            "fastapi",
            "pytest",
            "ruff",
            "prática",
            "backend",
            "revisão",
        ],
    }


@pytest.fixture
def tarefa_criada(client, dados_tarefa):
    response = client.post("/tarefas", json=dados_tarefa)

    return response


@pytest.fixture
def dados_atualizacao():
    return {
        "titulo": "Estudar testes com Pytest",
        "descricao": "Praticar os testes de atualização da API",
        "tags": ["python", "pytest", "atualização"],
        "concluida": True,
    }


@pytest.fixture
def dados_varias_tarefas():
    return [
        {
            "titulo": "Estudar Python avançado",
            "descricao": "Praticar os recursos da linguagem Python",
            "tags": ["python", "backend"],
        },
        {
            "titulo": "Revisar documentação FastAPI",
            "descricao": "Ler a documentação oficial do FastAPI",
            "tags": ["python", "fastapi"],
        },
        {
            "titulo": "Organizar atividades pessoais",
            "descricao": "Organizar as atividades da semana",
            "tags": ["pessoal", "organização", "python"],
        },
    ]


@pytest.fixture
def tarefas_criadas(client, dados_varias_tarefas):
    tarefas = []

    for dados in dados_varias_tarefas:
        response = client.post("/tarefas", json=dados)
        tarefas.append(response.json())

    return tarefas


@pytest.fixture
def tarefas_para_filtros(client, tarefas_criadas):
    tarefa = tarefas_criadas[1]

    response = client.put(
        f"/tarefas/{tarefa['id']}",
        json={
            "titulo": tarefa["titulo"],
            "descricao": tarefa["descricao"],
            "tags": tarefa["tags"],
            "concluida": True,
        },
    )

    tarefas_criadas[1] = response.json()

    return tarefas_criadas
