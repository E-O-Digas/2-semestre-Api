
import numpy as np

#Função assíncrona que pega as estatisticas da matéria C
@app.get("/getStats/")
async def getStats(notas_C):
    #Primeiro ela guarda todas as notas da matéria C de todos os alunos registrados
    notas_C = [aluno["notas"].get("C") for aluno in alunos if "C" in aluno["notas"]]
    #Depois ela utiliza as funções do numpy para calcular a media, mediana e desvio padrao das notas_C
    media = np.mean(notas_C)
    mediana = np.median(notas_C)
    desvio_padrao = np.std(notas_C)
    #Retorno os resultados
    return media, mediana, desvio_padrao

#Função assíncrona para pegar apenas os alunos que foram reprovados por tirar menos de 6
@app.get("/GetReprovados/")
async def getReprovados(notas):
    #lista para guardar os alunos
    resultado = []
    for aluno in Alunos:
        #pegar as notas dos alunos
        notas = aluno.get("notas", {}) 
        if notas:
            #se a nota não é nula e é menor do que 6 o aluno é inserido na lista
            if any(nota is not None and nota < 6 for nota in notas.values()):
                resultado.append(aluno)
    return resultado


@app.delete("/DeleteAlunosSemNotas")
def delete_alunos_sem_notas():
    #faz com que alunos possa ser acessado pela função
    global alunos
    #guarda os alunos que tem alguma nota no sistema
    alunos_com_notas = [aluno for aluno in alunos if aluno.get("notas")]
    #coloca apenas os alunos com notas em alunos
    alunos = alunos_com_notas
    #sobrepoe com os dados no sistema
    save_data(alunos)
    return {"Message": "Alunos sem notas removidos com sucesso"}
            

