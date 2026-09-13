# Esse SCHEMA representa o contrato que os objetos do tipo tarefa devem seguir
from pydantic import BaseModel, Field
from typing import Annotated
from uuid import UUID, uuid4
from datetime import datetime


# Base do schema das tarefas
class TarefaSchema(BaseModel):
    titulo: Annotated[str, Field(min_length=10, max_length=80)]
    descricao: str | None = None
    tags: list[str] = []


# As datas e o ID não devem ser especificamente para o banco de dados!
class TarefaSchemaBD(TarefaSchema):
    id: UUID = Field(default_factory=uuid4)
    concluida: bool = False
    data_criacao: datetime = Field(default_factory=datetime.now)
    data_atualizacao: datetime = Field(default_factory=datetime.now)


# O Schema de tarefa publico vai servir como base para as respostas
class TarefaSchemaPublico(BaseModel):
    id: UUID
    titulo: str
    descricao: str | None
    tags: list[str] = []
    concluida: bool = False
    data_criacao: datetime
    data_atualizacao: datetime


# Permite atualizar a tarefa
class TarefaSchemaAtualizado(TarefaSchema):
    concluida: bool

# Permite o retorno das respostas paginadas
class TarefaSchemaPaginada(BaseModel):
    pagina: int 
    limite: int
    total: int
    tarefas: list[TarefaSchemaPublico]
    