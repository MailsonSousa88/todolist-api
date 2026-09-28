import pytest
from fastapi.testclient import TestClient

from src.main import app


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
        "tags": ["python", "fastapi", "pytest", "ruff", "prática", "backend", "revisão"]        
    }

@pytest.fixture
def tarefa_criada(client, dados_tarefa):
    response = client.post("/tarefas", json=dados_tarefa)
    
    return response