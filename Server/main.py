from fastapi import FastAPI
from typing import Dict
import gc
import json
from pydantic import BaseModel

class Alunos(BaseModel):
    nome: str
    notas: Dict[str, float]
    id: str

app = FastAPI()

alunos_lista = []

@app.post("/create/")
async def create(aluno: Alunos):
    for nota in aluno.notas.values():
        if nota >= 0 and nota <= 10:
            aluno.notas= {materia : round(nota,1) for materia, nota in aluno.notas.items()}
           
            alunos_lista.append(aluno)
        else:
            return {"message": "Notas inválidas"}
            
    list_data= []

    for obj in gc.get_objects():
        if isinstance(obj, Alunos):
            list_data.append(obj.__dict__)
            
    try:
        file_out = open("dados.json", "xt")
        json.dump(list_data, file_out, indent= 4)
        file_out.close()

    except:
        file_out= open("dados.json", "at")
        json.dump(list_data, file_out, indent= 4)
        file_out.close()

@app.get("/getAll/")
async def getAll():
    with open("dados.json") as file:
        alunos_info= json.load(file)

    return alunos_info

@app.get("/getById/{alunoId}")
async def getById(alunoId):
    with open("dados.json") as file:
        alunos_info= json.load(file)

        for aluno in alunos_info:
            if aluno["id"] == alunoId:
                return aluno["nome"], aluno["notas"]
            
            else:
                return {"message": "Aluno não encontrado"}