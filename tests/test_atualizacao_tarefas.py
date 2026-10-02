from http import HTTPStatus


# T15 - Verificar se é possível atualizar o título e a descrição de uma tarefa.
def test_atualizar_titulo_e_descricao(
    client,
    tarefa_criada,
    dados_atualizacao,
):
    tarefa = tarefa_criada.json()

    response = client.put(
        f"/tarefas/{tarefa['id']}",
        json=dados_atualizacao,
    )
    tarefa_atualizada = response.json()

    assert response.status_code == HTTPStatus.OK
    assert tarefa_atualizada["titulo"] == dados_atualizacao["titulo"]
    assert tarefa_atualizada["descricao"] == dados_atualizacao["descricao"]


# T16 - Verificar se é possível alterar a tarefa de pendente para concluída.
def test_atualizar_tarefa_para_concluida(
    client,
    tarefa_criada,
    dados_atualizacao,
):
    tarefa = tarefa_criada.json()

    response = client.put(
        f"/tarefas/{tarefa['id']}",
        json=dados_atualizacao,
    )
    tarefa_atualizada = response.json()

    assert tarefa["concluida"] is False
    assert tarefa_atualizada["concluida"] is True


# T17 - Verificar se é possível atualizar as tags da tarefa.
def test_atualizar_tags_da_tarefa(client, tarefa_criada, dados_atualizacao):
    tarefa = tarefa_criada.json()

    response = client.put(
        f"/tarefas/{tarefa['id']}",
        json=dados_atualizacao,
    )
    tarefa_atualizada = response.json()

    assert tarefa_atualizada["tags"] == dados_atualizacao["tags"]


# T18 - Verificar se a data de atualização é modificada.
def test_modificar_data_atualizacao(client, tarefa_criada, dados_atualizacao):
    tarefa = tarefa_criada.json()

    response = client.put(
        f"/tarefas/{tarefa['id']}",
        json=dados_atualizacao,
    )
    tarefa_atualizada = response.json()

    assert tarefa_atualizada["data_atualizacao"] != tarefa["data_atualizacao"]


# T19 - Verificar se a data de criação permanece inalterada.
def test_preservar_data_criacao(client, tarefa_criada, dados_atualizacao):
    tarefa = tarefa_criada.json()

    response = client.put(
        f"/tarefas/{tarefa['id']}",
        json=dados_atualizacao,
    )
    tarefa_atualizada = response.json()

    assert tarefa_atualizada["data_criacao"] == tarefa["data_criacao"]


# T20 - Verificar se a atualização de uma tarefa inexistente retorna 404.
def test_atualizar_tarefa_inexistente(client, dados_atualizacao):
    response = client.put(
        "/tarefas/00000000-0000-0000-0000-000000000000",
        json=dados_atualizacao,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
