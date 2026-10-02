from http import HTTPStatus


# T08 - Verificar se a API retorna uma lista vazia quando não existem tarefas.
def test_listar_tarefas_sem_tarefas_cadastradas(client):
    response = client.get("/tarefas")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


# T09 - Verificar se a API retorna todas as tarefas cadastradas.
def test_listar_todas_as_tarefas(client, tarefas_criadas):
    response = client.get("/tarefas")
    tarefas_retornadas = response.json()

    for tarefa in tarefas_criadas:
        assert tarefa in tarefas_retornadas


# T10 - Verificar se cada tarefa retornada contém os campos esperados.
def test_tarefas_listadas_possuem_campos_obrigatorios(client, tarefas_criadas):
    response = client.get("/tarefas")
    tarefas = response.json()

    for tarefa in tarefas:
        assert set(tarefa.keys()) == {
            "id",
            "titulo",
            "descricao",
            "concluida",
            "tags",
            "data_criacao",
            "data_atualizacao",
        }


# T11 - Verificar se a quantidade retornada corresponde à quantidade cadastrada.
def test_quantidade_de_tarefas_listadas(client, tarefas_criadas):
    response = client.get("/tarefas")
    tarefas = response.json()

    assert len(tarefas) == len(tarefas_criadas)


# T12 - Verificar se é possível consultar uma tarefa existente pelo identificador.
def test_consultar_tarefa_existente(client, tarefa_criada):
    tarefa = tarefa_criada.json()

    response = client.get(f"/tarefas/{tarefa['id']}")

    assert response.status_code == HTTPStatus.OK


# T13 - Verificar se a tarefa consultada possui os dados corretos.
def test_consultar_dados_da_tarefa(client, tarefa_criada):
    tarefa = tarefa_criada.json()

    response = client.get(f"/tarefas/{tarefa['id']}")

    assert response.json() == tarefa


# T14 - Verificar se uma tarefa inexistente retorna 404 Not Found.
def test_consultar_tarefa_inexistente(client):
    response = client.get("/tarefas/00000000-0000-0000-0000-000000000000")

    assert response.status_code == HTTPStatus.NOT_FOUND
