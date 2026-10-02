from http import HTTPStatus


# T21 - Verificar se é possível excluir uma tarefa existente.
def test_excluir_tarefa_existente(client, tarefa_criada):
    tarefa = tarefa_criada.json()

    response = client.delete(f"/tarefas/{tarefa['id']}")

    assert response.status_code == HTTPStatus.NO_CONTENT


# T22 - Verificar se a exclusão retorna 204 No Content.
def test_excluir_tarefa_retorna_resposta_sem_conteudo(client, tarefa_criada):
    tarefa = tarefa_criada.json()

    response = client.delete(f"/tarefas/{tarefa['id']}")

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.content == b""


# T23 - Verificar se a tarefa excluída deixa de aparecer na listagem.
def test_tarefa_excluida_nao_aparece_na_listagem(client, tarefa_criada):
    tarefa = tarefa_criada.json()

    client.delete(f"/tarefas/{tarefa['id']}")
    response = client.get("/tarefas")

    assert response.json() == []


# T24 - Verificar se consultar a tarefa excluída retorna 404 Not Found.
def test_consultar_tarefa_excluida(client, tarefa_criada):
    tarefa = tarefa_criada.json()

    client.delete(f"/tarefas/{tarefa['id']}")
    response = client.get(f"/tarefas/{tarefa['id']}")

    assert response.status_code == HTTPStatus.NOT_FOUND


# T25 - Verificar se excluir uma tarefa inexistente retorna 404 Not Found.
def test_excluir_tarefa_inexistente(client):
    response = client.delete(
        "/tarefas/00000000-0000-0000-0000-000000000000"
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
