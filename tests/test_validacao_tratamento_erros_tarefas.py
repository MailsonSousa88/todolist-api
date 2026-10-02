from http import HTTPStatus


# T44 - Rejeitar a criação de uma tarefa sem título.
def test_criar_tarefa_sem_titulo(client):
    response = client.post(
        "/tarefas",
        json={
            "descricao": "Tarefa sem o campo obrigatório",
            "tags": ["python"],
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


# T45 - Retornar erro ao consultar uma tarefa inexistente.
def test_consultar_identificador_inexistente(client):
    response = client.get("/tarefas/00000000-0000-0000-0000-000000000000")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "A tarefa não foi encontrada..."


# T46 - Retornar erro ao atualizar uma tarefa inexistente.
def test_atualizar_identificador_inexistente(client, dados_atualizacao):
    response = client.put(
        "/tarefas/00000000-0000-0000-0000-000000000000",
        json=dados_atualizacao,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "A tarefa não foi encontrada."


# T47 - Retornar erro ao excluir uma tarefa inexistente.
def test_excluir_identificador_inexistente(client):
    response = client.delete(
        "/tarefas/00000000-0000-0000-0000-000000000000"
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "A tarefa não foi encontrada."


# T48 - Rejeitar um valor textual inválido no campo concluída.
def test_atualizar_com_tipo_invalido_em_concluida(
    client,
    tarefa_criada,
    dados_atualizacao,
):
    tarefa = tarefa_criada.json()
    dados_atualizacao["concluida"] = "valor inválido"

    response = client.put(
        f"/tarefas/{tarefa['id']}",
        json=dados_atualizacao,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "detail" in response.json()


# T49 - Rejeitar parâmetros de ordenação inválidos.
def test_parametros_de_ordenacao_invalidos(client):
    campo_invalido = client.get("/tarefas?ordenar_por=campo_invalido")
    ordem_invalida = client.get("/tarefas?ordem=lado_invalido")

    assert campo_invalido.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert ordem_invalida.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "detail" in campo_invalido.json()
    assert "detail" in ordem_invalida.json()
