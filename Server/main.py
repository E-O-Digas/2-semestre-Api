from fastapi import FastAPI
from typing import Dict
import numpy as np
import json, uuid
from pydantic import BaseModel

class Alunos(BaseModel):
    nome: str
    notas: Dict[str, float]

app = FastAPI()  #inicia a instancia APP, que contem as dependencias necessarias para rodar a api

#função assíncrona que carrega os dados do arquivo dados.json. Caso ele esteja vazio, retorna falso
async def load_data(): 
    try:
        with open("dados.json", "r") as file:
            return json.load(file)
        
    except:
        return []

#função sincrona que é utilizada para salvar dados em formato json no arquivo dados.json
def save_data(lista_alunos):
    with open("dados.json", "w") as file:
        json.dump(lista_alunos, file, indent= 4)


#função assíncrona utilizada para validar as notas dos alunos. Caso as notas estejam dentro do intervalo estipulado, retorna true, caso não estejam, retorna false
async def vld_notas(aluno):
    for nota in aluno.notas.values():
        if nota >= 0 and nota <=10:
            return True
        
        else:
            return False
        
#Função assíncrona utilizada para validar se o aluno ja foi cadastrado no arquivo dados.json, se utilizando da variável user_exist. 
#Caso o usuario ja esteja no arquivo a variavel user_exist passa a valer True, caso contrario a variavel sequer é criada, se a variavel for True, 
#isso quer dizer que o usuario existe então o usuario não pode ser cadastrado, por isso a def vld_aluno retornará False.
async def vld_aluno(aluno):
    alunos= await getAll()

    for qtd_aluno in range(0, len(alunos)):
        if str(aluno.nome) == str(alunos[qtd_aluno]["nome"]):
            user_exist= True

    try:
        if user_exist:
            return False
        
        else:
            return True
        
    except:
        return True
    

#Função assíncrona responsavel por chamar as funções de validação e, apos as validações necessárias, cria o objeto Alunos no arquivo dados.json
@app.post("/create/")
async def create(aluno: Alunos):
    id= str(uuid.uuid4())

    lista_alunos= await getAll()

    if await vld_aluno(aluno):
        if await vld_notas(aluno):
            notas= {materia : round(nota,1) for materia, nota in aluno.notas.items()}
                
            novo_aluno= {
                "id": id,
                "nome": aluno.nome,
                "notas": notas
            }

            lista_alunos.append(novo_aluno)

            save_data(lista_alunos)
           
        else:
            return {"message": "Notas inválidas, tente novamente."}
        
    else:
        return {"message": "Aluno ja cadastrado."}


#Função assíncrona que se utiliza da função assíncrona load_data para simplemente pegar todos os usuários que tem no arquivo dados.json
@app.get("/getAll/")
async def getAll():
    return await load_data()


#Função assíncrona que se utiliza da função assíncrona getAll() e de um parâmetro, alunoId, para buscar, por meio de um loop, um aluno específico com o id especificado no parâmetro.
@app.get("/getById/{alunoId}")
async def getById(alunoId):
    alunos_info= await getAll()

    for aluno in alunos_info:
        if aluno["id"] == alunoId:
            return aluno["nome"], aluno["notas"]
            
        else:
            return {"message": "Aluno não encontrado"}

#Função assíncrona que se utiliza da função assíncrona getAll() e de um parâmetro, nomeDisciplina, para buscar, por meio de um loop, 
#todas as notas de uma matéria e armazena-as em uma lista para ordenalas em ordem crescente. Retorna um dicionário com o nome da 
#disciplina desejada como chave, e uma lista, ordenada de forma crescente, como valor.
@app.get("/getNotas/{nomeDisciplina}")
async def getNotasByName(nomeDisciplina):
    alunos_info= await getAll()

    lista= []

    for aluno in alunos_info:
        notas_aluno= aluno["notas"]

        lista_alunos= [aluno["nome"], notas_aluno[f"{nomeDisciplina}"]]
        
        lista.append(lista_alunos)
        
    lista.sort(key= lambda x: x[1])

    return {nomeDisciplina: lista}

#Função assíncrona que pega as estatisticas da matéria C
@app.get("/getStats/{nomeDisciplina}")
async def getStats(nomeDisciplina):
    alunos= await getAll()

    #Primeiro ela guarda todas as notas da matéria C de todos os alunos registrados
    notas = [aluno["notas"].get(nomeDisciplina) for aluno in alunos if f"{nomeDisciplina}" in aluno["notas"]]

    #Depois ela utiliza as funções do numpy para calcular a media, mediana e desvio padrao das notas_C
    media = np.mean(notas)
    mediana = np.median(notas)
    desvio_padrao = np.std(notas)

    #Retorno os resultados
    return media, mediana, desvio_padrao

#Função assíncrona para pegar apenas os alunos que foram reprovados por tirar menos de 6
@app.get("/GetReprovados/")
async def getReprovados():
    alunos= await getAll()

    #lista para guardar os alunos
    resultado = []

    for aluno in alunos:
        #pegar as notas dos alunos
        notas = aluno.get("notas", {}) 

        if notas:
            #se a nota não é nula e é menor do que 6 o aluno é inserido na lista
            if any(nota is not None and nota < 6 for nota in notas.values()):

                resultado.append(aluno)

    return resultado


@app.delete("/DeleteAlunosSemNotas")
async def delete_alunos_sem_notas():
    #faz com que alunos possa ser acessado pela função
    alunos= await getAll()

    #guarda os alunos que tem alguma nota no sistema
    alunos_com_notas = [aluno for aluno in alunos if aluno.get("notas")]

    #coloca apenas os alunos com notas em alunos
    alunos = alunos_com_notas

    #sobrepoe com os dados no sistema
    save_data(alunos)

    return {"Message": "Alunos sem notas removidos com sucesso"}
            

