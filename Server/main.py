from fastapi import FastAPI
import model

app = FastAPI()

@app.get()
async def root():
    return{"message", "aaaaaa"}

alunos= []

@app.get("/tasks")
async def create(aluno: model.Aluno):
    alunos.append(aluno)   

