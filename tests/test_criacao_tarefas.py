from http import HTTPStatus
from uuid import UUID


# T01 - Testa se a tarefa foi criada, e se o status code foi adequado (201) - CREATED
def test_criar_tarefa_com_dados_validos(tarefa_criada):

    assert tarefa_criada.status_code == HTTPStatus.CREATED


# T02 - Verificar se a tarefa retornada contém os campos obrigatórios: id, titulo, descricao, concluida, tags, data_criacao e data_atualizacao.
def test_tarefa_com_campos_obrigatorios(tarefa_criada):

    tarefa = tarefa_criada.json()

    # SET - Essa função é adequada quando a ordem das CHAVES não é tão relevante
    assert set(tarefa.keys()) == {
        "id",
        "titulo",
        "descricao",
        "concluida",
        "tags",
        "data_criacao",
        "data_atualizacao",
    }


# T03 - Verificar se o identificador da tarefa é gerado automaticamente.
def test_tarefa_com_indentificador_presente(tarefa_criada, dados_tarefa):

    tarefa = tarefa_criada.json()

    assert "id" not in dados_tarefa

    id_gerado = UUID(tarefa["id"])

    assert isinstance(id_gerado, UUID)


# T04 - Verificar se a tarefa é criada com concluida = false.
def test_tarefa_criada_como_pendente(tarefa_criada):
    
    tarefa = tarefa_criada.json()
    
    assert tarefa["concluida"] is False
    

# T05 - Verificar se as datas de criação e atualização são preenchidas automaticamente.
def test_tarefa_com_datas_presente(tarefa_criada):
    
    tarefa = tarefa_criada.json()
    
    assert tarefa["data_criacao"] is not None
    assert tarefa["data_atualizacao"] is not None
    assert tarefa["data_criacao"] != ""
    assert tarefa["data_atualizacao"] != ""
    

# T06 - Verificar se é possível criar uma tarefa com várias tags.
def test_tarefa_com_varias_tags(client, dados_tarefa_tags):
    response = client.post(
        "/tarefas",
        json=dados_tarefa_tags,
    )

    tarefa = response.json()

    assert tarefa["tags"] == dados_tarefa_tags["tags"]
    assert len(tarefa["tags"]) > 1
    
# T07 - Verificar se a API rejeita uma tarefa sem título, retornando um código HTTP de erro apropriado.
def test_tarefa_sem_campo_titulo(client):
    response = client.post("/tarefas", json={
        "descricao": "Revisar e praticar os ensinamentos sobre programação para internet II",
        "tags": ["python", "fastapi"],
    })
    
    assert response.status_code == 422
