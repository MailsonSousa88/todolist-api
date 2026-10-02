# T36 - Ordenar tarefas por data de criação em ordem crescente.
def test_ordenar_por_data_criacao_crescente(client, tarefas_criadas):
    response = client.get("/tarefas?ordenar_por=data_criacao&ordem=asc")
    tarefas = response.json()
    datas = [tarefa["data_criacao"] for tarefa in tarefas]

    assert datas == sorted(datas)


# T37 - Ordenar tarefas por data de criação em ordem decrescente.
def test_ordenar_por_data_criacao_decrescente(client, tarefas_criadas):
    response = client.get("/tarefas?ordenar_por=data_criacao&ordem=desc")
    tarefas = response.json()
    datas = [tarefa["data_criacao"] for tarefa in tarefas]

    assert datas == sorted(datas, reverse=True)


# T38 - Ordenar tarefas por data de atualização em ordem crescente.
def test_ordenar_por_data_atualizacao_crescente(client, tarefas_criadas):
    response = client.get("/tarefas?ordenar_por=data_atualizacao&ordem=asc")
    tarefas = response.json()
    datas = [tarefa["data_atualizacao"] for tarefa in tarefas]

    assert datas == sorted(datas)


# T39 - Ordenar tarefas por data de atualização em ordem decrescente.
def test_ordenar_por_data_atualizacao_decrescente(client, tarefas_criadas):
    response = client.get("/tarefas?ordenar_por=data_atualizacao&ordem=desc")
    tarefas = response.json()
    datas = [tarefa["data_atualizacao"] for tarefa in tarefas]

    assert datas == sorted(datas, reverse=True)


# T40 - Ordenar tarefas por título em ordem crescente.
def test_ordenar_por_titulo_crescente(client, tarefas_criadas):
    response = client.get("/tarefas?ordenar_por=titulo&ordem=asc")
    tarefas = response.json()
    titulos = [tarefa["titulo"] for tarefa in tarefas]

    assert titulos == sorted(titulos)


# T41 - Ordenar tarefas por título em ordem decrescente.
def test_ordenar_por_titulo_decrescente(client, tarefas_criadas):
    response = client.get("/tarefas?ordenar_por=titulo&ordem=desc")
    tarefas = response.json()
    titulos = [tarefa["titulo"] for tarefa in tarefas]

    assert titulos == sorted(titulos, reverse=True)


# T42 - Ordenar tarefas por identificador em ordem crescente.
def test_ordenar_por_id_crescente(client, tarefas_criadas):
    response = client.get("/tarefas?ordenar_por=id&ordem=asc")
    tarefas = response.json()
    identificadores = [tarefa["id"] for tarefa in tarefas]

    assert identificadores == sorted(identificadores)


# T43 - Ordenar tarefas por identificador em ordem decrescente.
def test_ordenar_por_id_decrescente(client, tarefas_criadas):
    response = client.get("/tarefas?ordenar_por=id&ordem=desc")
    tarefas = response.json()
    identificadores = [tarefa["id"] for tarefa in tarefas]

    assert identificadores == sorted(identificadores, reverse=True)
