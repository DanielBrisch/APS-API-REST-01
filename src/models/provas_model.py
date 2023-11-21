from typing import List

from sqlmodel import Field, Relationship, SQLModel


class Provas(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    descricao: str
    data_prova: str
    q1: str
    q2: str
    q3: str
    q4: str
    q5: str
    q6: str
    q7: str
    q8: str
    q9: str
    q10: str
    resultados: List["Resultados"] = Relationship(back_populates="provas")
