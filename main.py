from fastapi import FastAPI, HTTPException, Query
from http import HTTPStatus
from tarefa_schema import (
    TarefaSchema,
    TarefaSchemaBD,
    TarefaSchemaPublico,
    TarefaSchemaAtualizado,
    TarefaSchemaPaginada
)
from uuid import UUID
from repositorio_de_tarefas import listaDeTarefas
from datetime import date, datetime
from typing import Annotated, Literal

app = FastAPI()

# ROTAS: GET


@app.get(
    "/",
    summary="Mensagem de boas-vindas",
    description="Retorna uma mensagem de boas-vindas da API.",
)
def root():
    return {"mensagem": "Ola, mundo!"}


# Listar todas as tarefas


@app.get(
    "/tarefas",
    response_model=list[TarefaSchemaPublico] | TarefaSchemaPaginada,
    status_code=HTTPStatus.OK,
    summary="Listar Tarefas",
    description="Lista tarefas com filtros por situação, tag, título e período de criação, além de ordenação e paginação opcional.",
)
def listar_tarefas(
    concluida: Annotated[
        bool | None,
        Query(
            title="Filtro de Situação", description="Filtra todas tarefas por situação"
        ),
    ] = None,
    tag: Annotated[
        str | None,
        Query(title="Filtro de Tags", description="Filtra todas as tarefas pela tag"),
    ] = None,
    titulo: Annotated[
        str | None,
        Query(
            title="Filtro de Titulos",
            description="Filtra todas tarefas através do titulo.",
        ),
    ] = None,
    data_inicio: Annotated[
        date | None,
        Query(description="Data inicial de criação, inclusive, no formato YYYY-MM-DD"),
    ] = None,
    data_fim: Annotated[
        date | None,
        Query(description="Data final de criação, inclusive, no formato YYYY-MM-DD"),
    ] = None,
    ordenar_por: Annotated[
        Literal["id", "titulo", "data_criacao", "data_atualizacao"],
        Query(description="Campo usado para ordenar as tarefas"),
    ] = "id",
    ordem: Annotated[
        Literal["asc", "desc"],
        Query(description="Direção da ordenação: crescente ou decrescente"),
    ] = "asc",
    pagina: Annotated[int | None, Query(ge=1, description="Define o número da página")] = None,
    limite: Annotated[
        int | None, Query(ge=1, description="Define o limite de tarefas que serão exibidas")
    ] = None,
) -> list[TarefaSchemaBD] | dict:

    if data_inicio is not None and data_fim is not None:
        if data_inicio > data_fim:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="A data inicial não pode ser posterior à data final.",
            )

    paginada = pagina is not None or limite is not None
    pagina = pagina if pagina is not None else 1
    limite = limite if limite is not None else 5

    # Usaremos a propriedade de inicio:fim dos arrays
    inicio: int = (pagina - 1) * limite
    fim: int = inicio + limite

    if (
        concluida is None
        and tag is None
        and titulo is None
        and data_inicio is None
        and data_fim is None
    ):

        # Sem filtros: ordena todas as tarefas.
        tarefas_ordenadas_sem_filtros = sorted(
            listaDeTarefas,
            key=lambda tarefa: getattr(tarefa, ordenar_por),
            reverse=(ordem == "desc"),
        )

        if not paginada:
            return tarefas_ordenadas_sem_filtros

        return {
            "pagina": pagina,
            "limite": limite,
            "total": len(tarefas_ordenadas_sem_filtros),
            "tarefas": tarefas_ordenadas_sem_filtros[inicio:fim],
        }

    tarefas_filtradas: list[TarefaSchemaBD] = []

    # 1. Loop de verificação
    for tarefa in listaDeTarefas:
        # 1.1 Verifica se a query "concluida" foi informado
        if concluida is not None:
            if tarefa.concluida != concluida:
                continue
        # 1.2 Verifica se a query "tag" foi informado
        if tag is not None:
            if tag not in tarefa.tags:
                continue
        # 1.3 Verifica se a query "titulo" foi informado
        if titulo is not None:
            if titulo.lower() not in tarefa.titulo.lower():
                continue

        # Compara somente a data para incluir todos os horários do dia final.
        data_da_tarefa = tarefa.data_criacao.date()

        if data_inicio is not None:
            if data_da_tarefa < data_inicio:
                continue

        if data_fim is not None:
            if data_da_tarefa > data_fim:
                continue

        tarefas_filtradas.append(tarefa)

    # Com filtros: ordena somente as tarefas selecionadas.
    tarefas_ordenadas_com_filtros = sorted(
        tarefas_filtradas,
        key=lambda tarefa: getattr(tarefa, ordenar_por),
        reverse=(ordem == "desc"),
    )

    if not paginada:
        return tarefas_ordenadas_com_filtros

    return {
        "pagina": pagina,
        "limite": limite,
        "total": len(tarefas_ordenadas_com_filtros),
        "tarefas": tarefas_ordenadas_com_filtros[inicio:fim],
    }


# Listar tarefa por ID


@app.get(
    "/tarefas/{id}",
    response_model=TarefaSchemaPublico,
    status_code=HTTPStatus.OK,
    summary="Consultar tarefa por ID",
    description="Consulta uma tarefa pelo seu UUID. Retorna 404 se a tarefa não existir.",
)
def listar_tarefa_por_id(id: UUID):
    for tarefa in listaDeTarefas:
        if tarefa.id == id:
            return tarefa

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="A tarefa não foi encontrada..."
    )


# ROTAS: POST


@app.post(
    "/tarefas",
    response_model=TarefaSchemaPublico,
    status_code=HTTPStatus.CREATED,
    summary="Criar tarefa",
    description="Cria uma tarefa com título, descrição e tags. Gera automaticamente o ID e as datas e define a tarefa como pendente.",
)
def criar_tarefa(tarefa: TarefaSchema):
    nova_tarefa = TarefaSchemaBD(**tarefa.model_dump())
    listaDeTarefas.append(nova_tarefa)

    return nova_tarefa


# ROTAS: PUT


@app.put(
    "/tarefas/{id}",
    response_model=TarefaSchemaPublico,
    status_code=HTTPStatus.OK,
    summary="Atualizar tarefa",
    description="Atualiza título, descrição, tags e situação de uma tarefa pelo UUID. Preserva a data de criação e renova a data de atualização. Retorna 404 se a tarefa não existir.",
)
def atualizar_tarefa(id: UUID, tarefa: TarefaSchemaAtualizado):
    for idx, t in enumerate(listaDeTarefas):
        if t.id == id:
            tarefa_atualizada = TarefaSchemaBD(
                id=id, data_criacao=t.data_criacao, **tarefa.model_dump()
            )
            listaDeTarefas[idx] = tarefa_atualizada

            return tarefa_atualizada

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="A tarefa não foi encontrada."
    )


# ROTAS: DELETE


@app.delete(
    "/tarefas/{id}",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Excluir tarefa",
    description="Exclui uma tarefa pelo seu UUID. Retorna 204 sem conteúdo em caso de sucesso ou 404 se a tarefa não existir.",
)
def excluir_tarefa(id: UUID):
    for idx, t in enumerate(listaDeTarefas):
        if t.id == id:
            del listaDeTarefas[idx]
            return

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="A tarefa não foi encontrada."
    )
