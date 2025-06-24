from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime
from enum import Enum
import uuid
from uuid import UUID


app = FastAPI()

projetos = []



class PrioridadeEnum(int, Enum):
    alta = 1
    media = 2 
    baixa = 3
    
class StatusEnum(str, Enum):
    planejado = 'Planejado'
    andamento = 'Em Andamento'
    concluido = 'Concluído'
    cancelado = 'Cancelado'


class ProjetoCreate(BaseModel): 
    titulo: str 
    descricao: Optional[str] = None
    prioridade: PrioridadeEnum
    status: StatusEnum
    
class Projeto(ProjetoCreate):
    id: UUID = Field(default_factory=uuid.uuid4)
    data_de_criacao: str
    
# HOME
@ app.get('/')
def home():
    return {'mensagem' : 'Olá, Seja Bem-Vindo!!'}
    
# CRIAÇÃO DE PROJETOS
@app.post('/projetos')
def criar_projeto(projeto: ProjetoCreate):

    data_de_criacao = datetime.utcnow()
    data_formatada = data_de_criacao.strftime('%d/%m/%Y %H:%M:%S')
    novo_projeto = Projeto(
        id = uuid.uuid4(),
        data_de_criacao = data_formatada,
        **projeto.dict() 
    )
    

    projetos.append(novo_projeto)
    return novo_projeto

# LISTAR PROJETOS
@app.get('/projetos', response_model = list[Projeto])
def listar_projetos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[StatusEnum] = None,
    prioridade: Optional[PrioridadeEnum] = None
):
    resultados = projetos
    
    if status:
        projetos_filtrados = []
        for proj in resultados:
            if proj.status == status:
                projetos_filtrados.append(proj)
        resultados = projetos_filtrados
            
    if prioridade:
        projetos_filtrados = []
        for proj in resultados:
            if proj.prioridade == prioridade:
                projetos_filtrados.append(proj)
        resultados = projetos_filtrados
    
    if not resultados:
        raise HTTPException (status_code = 404, detail = 'Nenhum projeto foi encontrado')
    
    return resultados[skip: skip + limit]

# BUSCA POR ID
@app.get('/projetos/{projeto_id}', response_model = Projeto)
def buscar_projeto(projeto_id: UUID):
    for proj in projetos:
        if proj.id == projeto_id:
            return proj
    raise  HTTPException(status_code=404, detail= 'Projeto não encontrado')

# DELETE 
@app.delete('/projetos/{projeto_id}', response_model = Projeto)
def deletar_projeto(projeto_id: UUID):
    for proj in projetos:
        if proj.id == projeto_id:
            projetos.remove(proj)
            return proj
            
    raise  HTTPException(status_code=404, detail= 'Projeto não encontrado')

# ATUALIZAR
@app.put("/projetos/{projeto_id}", response_model=Projeto)
def atualizar_projeto(projeto_id: UUID, novo_dados: ProjetoCreate):
    for projeto in projetos:
        if projeto.id == projeto_id:
            projeto.titulo = novo_dados.titulo
            projeto.descricao = novo_dados.descricao
            projeto.prioridade = novo_dados.prioridade
            projeto.status = novo_dados.status
            return projeto
    raise HTTPException(status_code=404, detail="Projeto não encontrado")