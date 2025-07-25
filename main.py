from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()

class Pessoa(BaseModel):
    nome : str
    idade : int
    
 lista_pessoa = []   

@app.get('/')
def read_root():
    return {"mensagem": "Bem-Vindo à sua primeira API com FastAPI!"}

@app.get('/nome/{nome}')
def digite_nome(nome: str):
    return {"mensagem": f"Olá, eu me chamo {nome}"}

@app.post('/pessoa')
async def registro(pessoa : Pessoa):
    texto = f'nome : {pessoa.nome} , idade : {pessoa.idade}'
    return {"resul": texto}