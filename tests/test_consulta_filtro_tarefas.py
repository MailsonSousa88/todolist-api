from http import HTTPStatus


# T26 - Filtrar tarefas concluídas com resultado encontrado.
def test_filtrar_tarefas_concluidas(client, tarefas_para_filtros):
    response = client.get("/tarefas?concluida=true")
    tarefas = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(tarefas) == 1
    assert tarefas[0]["concluida"] is True


# T27 - Filtrar tarefas concluídas sem resultado encontrado.
def test_filtrar_tarefas_concluidas_sem_resultado(client, tarefa_criada):
    response = client.get("/tarefas?concluida=true")

    assert response.json() == []


# T28 - Filtrar tarefas pendentes com resultado encontrado.
def test_filtrar_tarefas_pendentes(client, tarefas_para_filtros):
    response = client.get("/tarefas?concluida=false")
    tarefas = response.json()

    assert len(tarefas) == 2

    for tarefa in tarefas:
        assert tarefa["concluida"] is False


# T29 - Filtrar tarefas pendentes sem resultado encontrado.
def test_filtrar_tarefas_pendentes_sem_resultado(
    client,
    tarefa_criada,
    dados_atualizacao,
):
    tarefa = tarefa_criada.json()

    client.put(
        f"/tarefas/{tarefa['id']}",
        json=dados_atualizacao,
    )
    response = client.get("/tarefas?concluida=false")

    assert response.json() == []


# T30 - Filtrar tarefas por tag com resultados encontrados.
def test_filtrar_tarefas_por_tag(client, tarefas_para_filtros):
    response = client.get("/tarefas?tag=python")
    tarefas = response.json()

    assert len(tarefas) == 3

    for tarefa in tarefas:
        assert "python" in tarefa["tags"]


# T31 - Filtrar tarefas por tag sem resultado encontrado.
def test_filtrar_tarefas_por_tag_sem_resultado(client, tarefas_para_filtros):
    response = client.get("/tarefas?tag=javascript")

    assert response.json() == []


# T32 - Filtrar tarefas por título com resultado encontrado.
def test_filtrar_tarefas_por_titulo(client, tarefas_para_filtros):
    response = client.get("/tarefas?titulo=python")
    tarefas = response.json()

    assert len(tarefas) == 1
    assert "python" in tarefas[0]["titulo"].lower()


# T33 - Filtrar tarefas por título sem resultado encontrado.
def test_filtrar_tarefas_por_titulo_sem_resultado(client, tarefas_para_filtros):
    response = client.get("/tarefas?titulo=javascript")

    assert response.json() == []


# T34 - Combinar os filtros de situação e tag.
def test_combinar_filtros_de_situacao_e_tag(client, tarefas_para_filtros):
    response = client.get("/tarefas?concluida=false&tag=python")
    tarefas = response.json()

    assert len(tarefas) == 2

    for tarefa in tarefas:
        assert tarefa["concluida"] is False
        assert "python" in tarefa["tags"]


# T35 - Combinar filtros com ordenação por data de criação decrescente.
def test_combinar_filtros_com_ordenacao(client, tarefas_para_filtros):
    response = client.get(
        "/tarefas?concluida=false&tag=python"
        "&ordenar_por=data_criacao&ordem=desc"
    )
    tarefas = response.json()
    datas = [tarefa["data_criacao"] for tarefa in tarefas]

    assert len(tarefas) == 2
    assert datas == sorted(datas, reverse=True)
