from pydantic import BaseModel

class Aluno(BaseModel):
    nome: str
    nota: float